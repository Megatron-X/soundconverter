pkgname=soundconverter-x
pkgver=4.2.2
pkgrel=2
_commit=bf6f1e8509f38222e397a40006d5d5a9780444ce
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
  'python-mutagen'
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
sha256sums=('f68e7ede61c734c0ccd1745b1986bef602c742a59916b18489bc1f361a6aa0af')

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
