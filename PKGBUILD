pkgname=soundconverter-x
pkgver=4.2.2
pkgrel=1
pkgdesc='GNOME sound converter with advanced codec controls and high-quality GStreamer encoding options'
arch=('any')
url='https://github.com/Megatron-X/soundconverter'
license=('GPL-3.0-or-later')

depends=(
  'gst-plugins-base'
  'gst-plugins-good'
  'gst-plugins-bad'
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

source=("$pkgname-$pkgver.tar.gz::$url/archive/refs/tags/$pkgver.tar.gz")
sha256sums=('d2e7a0bb06446f584dde44ab9267702efe4d93b2a26bdc8fb55d111e318d4ead')

build() {
  arch-meson "soundconverter-$pkgver" build
  meson compile -C build
}

check() {
  meson test -C build --print-errorlogs
}

package() {
  meson install -C build --destdir "$pkgdir"
}
