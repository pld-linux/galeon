# Note that this is NOT a relocatable package
%define ver      0.4
%define rel      1
%define prefix   /usr

Summary:   Galeon
Name:      galeon
Version:   %ver
Release:   %rel
Copyright: GPL
Group:     Applications/Internet
Source:    galeon-%{PACKAGE_VERSION}.tar.gz
URL:       http://galeon.sourceforge.net
BuildRoot: /tmp/galeon-%{PACKAGE_VERSION}-root
Packager:  Marco Pesenti Gritti <mpeseng@tin.it>
Autoreq: 0
Requires: gnome-libs >= 1.0.0
Requires: ORBit >= 0.4.0

Docdir: %{prefix}/doc

%description
Gnome browser based on Gecko (Mozilla rendering engine)
%prep
%setup

%build
if [ ! -f configure ]; then
  CFLAGS="$RPM_OPT_FLAGS" ./autogen.sh --prefix=%{prefix} \
    --with-gnome --without-debug --sysconfdir=/etc
else
  CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%{prefix} \
    --with-gnome --without-debug --sysconfdir=/etc
fi

if [ "$SMP" != "" ]; then
  (make "MAKE=make -k -j $SMP"; exit 0)
  make
else
  make
fi

%install
rm -rf $RPM_BUILD_ROOT

make prefix=$RPM_BUILD_ROOT%{prefix} sysconfdir=$RPM_BUILD_ROOT/etc install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)

%doc AUTHORS COPYING ChangeLog NEWS README
%{prefix}/bin/*
%{prefix}/share/*
