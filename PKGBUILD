pkgname=soundconverter-x
pkgver=4.2.2
pkgrel=2
_commit=bef0f99b042a770e6bc84ba1bcbfcdaffe0d722c
pkgdesc='GNOME sound converter with advanced codec controls and high-quality GStreamer encoding options'
arch=('any')
url='https://github.com/Megatron-X/soundconverter'
license=('GPL-3.0-or-later')

depends=(
  'gst-plugins-base'
  'gst-plugins-good'
  'gst-plugins-bad'
  'gst-plugins-ugly'
  'gst-python'
  'gtk3'
  'python-gobject'
)

optdepends=(
  'gst-libav: additional codec support including WMA'
)

makedepends=(
  'meson'
  'gettext'
)

provides=('soundconverter')
conflicts=('soundconverter')

source=("$pkgname-$pkgver-$_commit.tar.gz::$url/archive/$_commit.tar.gz")
sha256sums=('1d676067c038bb8e836ea13438de58b2ad6f1e5ad6331aa3f8ce2bb116a80092')

build() {
  arch-meson "soundconverter-$_commit" build
  meson compile -C build
}

check() {
  meson test -C build --print-errorlogs
}

package() {
  meson install -C build --destdir "$pkgdir"
}
