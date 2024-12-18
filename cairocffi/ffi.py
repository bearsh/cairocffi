"""
    cairocffi.ffi
    ~~~~~~~~~~~~~

    Build the cffi bindings

    :copyright: Copyright 2013-2019 by Simon Sapin
    :license: BSD, see LICENSE for details.

"""

from cffi import FFI

from . import constants

# Primary cffi definitions
ffi = FFI()
ffi.cdef(constants._CAIRO_HEADERS)

# include xcffib cffi definitions for cairo xcb support
try:
    from xcffib.ffi import ffi as xcb_ffi
except (ImportError, OSError):
    pass
else:
    ffi.include(xcb_ffi)
    ffi.cdef(constants._CAIRO_XCB_HEADERS)

# gdk pixbuf cffi definitions
ffi_pixbuf = FFI()
ffi_pixbuf.include(ffi)
ffi_pixbuf.cdef('''
    typedef unsigned long   gsize;
    typedef unsigned int    guint32;
    typedef unsigned int    guint;
    typedef unsigned char   guchar;
    typedef char            gchar;
    typedef int             gint;
    typedef gint            gboolean;
    typedef guint32         GQuark;
    typedef void*           gpointer;
    typedef ...             GdkPixbufLoader;
    typedef ...             GdkPixbufFormat;
    typedef ...             GdkPixbuf;
    typedef struct {
        GQuark              domain;
        gint                code;
        gchar              *message;
    } GError;
    typedef enum {
        GDK_COLORSPACE_RGB
    } GdkColorspace;


    GdkPixbufLoader * gdk_pixbuf_loader_new          (void);
    GdkPixbufFormat * gdk_pixbuf_loader_get_format   (GdkPixbufLoader *loader);
    GdkPixbuf *       gdk_pixbuf_loader_get_pixbuf   (GdkPixbufLoader *loader);
    gboolean          gdk_pixbuf_loader_write        (
        GdkPixbufLoader *loader, const guchar *buf, gsize count,
        GError **error);
    void              gdk_pixbuf_loader_set_size (
        GdkPixbufLoader *loader, int width, int height);
    gboolean          gdk_pixbuf_loader_close        (
        GdkPixbufLoader *loader, GError **error);

    gchar *           gdk_pixbuf_format_get_name     (GdkPixbufFormat *format);

    GdkColorspace     gdk_pixbuf_get_colorspace      (const GdkPixbuf *pixbuf);
    int               gdk_pixbuf_get_n_channels      (const GdkPixbuf *pixbuf);
    gboolean          gdk_pixbuf_get_has_alpha       (const GdkPixbuf *pixbuf);
    int               gdk_pixbuf_get_bits_per_sample (const GdkPixbuf *pixbuf);
    int               gdk_pixbuf_get_width           (const GdkPixbuf *pixbuf);
    int               gdk_pixbuf_get_height          (const GdkPixbuf *pixbuf);
    int               gdk_pixbuf_get_rowstride       (const GdkPixbuf *pixbuf);
    guchar *          gdk_pixbuf_get_pixels          (const GdkPixbuf *pixbuf);
    gsize             gdk_pixbuf_get_byte_length     (const GdkPixbuf *pixbuf);
    gboolean          gdk_pixbuf_save_to_buffer      (
        GdkPixbuf *pixbuf, gchar **buffer, gsize *buffer_size,
        const char *type, GError **error, ...);

    void              gdk_cairo_set_source_pixbuf    (
        cairo_t *cr, const GdkPixbuf *pixbuf,
        double pixbuf_x, double pixbuf_y);


    void              g_object_ref                   (gpointer object);
    void              g_object_unref                 (gpointer object);
    void              g_error_free                   (GError *error);
    void              g_type_init                    (void);
''')
