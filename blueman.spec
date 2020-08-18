Name:		blueman
Summary:	GTK+ Bluetooth Manager
License:	GPLv2+
Version:	2.1.3
Release:	1
URL:		https://github.com/blueman-project/blueman
Source0:	%{URL}/releases/download/%{version}/blueman-%{version}.tar.gz

BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(pygobject-3.0)
BuildRequires:	pkgconfig(bluez)
BuildRequires:	pkgconfig(polkit-agent-1)
BuildRequires:	pkgconfig(python3)
BuildRequires:	desktop-file-utils
BuildRequires:	intltool >= 0.35.0
BuildRequires:	iproute
BuildRequires:	python3-Cython >= 0.21
BuildRequires:	python3-dbus
BuildRequires:	systemd

%{?systemd_requires}
Requires:	python3-gobject-base
Requires:	bluez
Requires:	bluez-obexd
Requires:	dconf
Requires:	dbus
Requires:	iproute
Requires:	python3-dbus
Requires:	pulseaudio-libs-glib2
Requires:	pulseaudio-module-bluetooth

Provides:	dbus-bluez-pin-helper
Obsoletes:	blueman-nautilus

%description
Blueman is a tool to use Bluetooth devices. It is designed to provide simple,
yet effective means for controlling BlueZ API and simplifying bluetooth tasks
such as:
- Connecting to 3G/EDGE/GPRS via dial-up
- Connecting to/Creating bluetooth networks
- Connecting to input devices
- Connecting to audio devices
- Sending/Receiving files via OBEX
- Pairing


%prep
%setup -q
sed -e 's|/usr/sbin/bluetoothd|%{_libexecdir}/bluetooth/bluetoothd|g' -i apps/blueman-report.in

%build
export PYTHON=%{_bindir}/python3

# Override the "_configure" macro - the name of the script
# in this repo is ./autogen.sh, not ./configure
%global _configure ./autogen.sh
%configure --disable-static \
           --enable-thunar-sendto=no \
           --disable-schemas-compile \
           --disable-appindicator
make %{?_smp_mflags}


%install
%{make_install}

find %{buildroot} -name '*.la' -exec rm -f {} ';'
rm -rf %{buildroot}%{_datadir}/doc/blueman/

%find_lang blueman

# we need to own this, not only because of SELinux
mkdir -p %{buildroot}%{_sharedstatedir}/blueman
touch %{buildroot}%{_sharedstatedir}/blueman/network.state


%check
desktop-file-validate %{buildroot}%{_sysconfdir}/xdg/autostart/blueman.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/blueman-*.desktop


%post
%systemd_post blueman-mechanism.service
%systemd_user_post blueman-applet.service

%postun
%systemd_postun_with_restart blueman-mechanism.service

%preun
%systemd_preun blueman-mechanism.service
%systemd_user_preun blueman-applet.service


%files -f blueman.lang
%doc CHANGELOG.md FAQ README.md
%license COPYING
%{_bindir}/*
%{python3_sitelib}/blueman/
%{python3_sitearch}/*.so
%{_libexecdir}/blueman-*
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.blueman.Mechanism.conf
%{_sysconfdir}/xdg/autostart/blueman.desktop
%{_datadir}/applications/blueman-*.desktop
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/pixmaps/blueman/
%{_datadir}/blueman/
%{_datadir}/dbus-1/services/org.blueman.Applet.service
%{_datadir}/dbus-1/system-services/org.blueman.Mechanism.service
%{_datadir}/glib-2.0/schemas/*
%{_datadir}/polkit-1/actions/org.blueman.policy
%{_datadir}/polkit-1/rules.d/blueman.rules
%{_mandir}/man1/*
%{_unitdir}/blueman-mechanism.service
%{_userunitdir}/blueman-applet.service
%dir %{_sharedstatedir}/blueman
%ghost %attr(0644,root,root) %{_sharedstatedir}/blueman/network.state


%changelog
* Wed Sep 16 2020 Luke Yue <lukedyue@gmail.com> - 1:2.1.3-1
- Package init
