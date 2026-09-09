pkgname=soundconverter-x
pkgver=4.2.2
pkgrel=2
_commit=a5393bc9231c13d8a7242bb8c4e08df21e8aa24d
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

source=("$pkgname-$pkgver-$_commit.tar.gz::$url/archive/$_commit.tar.gz")
sha256sums=('3a51741b1529f3a36a109eacfdfb54e4e60008956c5e9cf2f3e5393355ffb1b0')

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
