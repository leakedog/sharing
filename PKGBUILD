# Maintainers: (refer to the gitlab page)
pkgname="raat-server"
pkgver="1.0.0"
pkgrel=1
epoch=
pkgdesc="Remote Archlinux Android Tool (server) for managing and connecting to VNC sessions"
arch=('any')
url="https://github.com/Student-Team-Projects/RAAT-Server"
license=('GPL')
groups=()
depends=('cinnamon' 'tigervnc' 'openssh' 'lxde-common' 'vncviewer') # Dependencies for both scripts
makedepends=()
checkdepends=()
optdepends=()
provides=()
conflicts=()
replaces=()
backup=()
options=()
install=
changelog=
source=("raat-server.sh" "raat-connect.sh") # Include both scripts
noextract=()
sha256sums=('SKIP' 'SKIP') # Replace 'SKIP' with actual checksums if needed
validpgpkeys=()

package() {
    # Create the bin directory in the package
    mkdir -p "${pkgdir}/usr/bin"

    # Install the raat-server script
    cp "${srcdir}/raat-server.sh" "${pkgdir}/usr/bin/raat-server"
    chmod +x "${pkgdir}/usr/bin/raat-server"

    # Install the raat-connect script
    cp "${srcdir}/raat-connect.sh" "${pkgdir}/usr/bin/raat-connect"
    chmod +x "${pkgdir}/usr/bin/raat-connect"
}
