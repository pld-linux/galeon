%define ver      0.4
%define sver     a
%define rel      1
%define prefix   /usr
Summary:	Galeon
Name:		galeon
Version:	%{ver}%{sver}
Release:	%{rel}
License:	GPL
Group:		X11/Applications/Networking
Group(pl):	X11/Aplikacje/Sieciowe
Source0:	http://download.sourceforge.net/galeon/%{name}-%{version}.tar.gz
URL:		http://galeon.sourceforge.net
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Autoreq:	0
Requires:	gnome-libs >= 1.0.0
Requires:	ORBit >= 0.4.0
BuildRequires:	libxml-devel >= 1.8.7


%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
Gnome browser based on Gecko (Mozilla rendering engine)
%prep
%setup -q -n %{name}-%{ver}

%build
if [ ! -f configure ]; then
  CFLAGS="$RPM_OPT_FLAGS" ./autogen.sh --prefix=%{_prefix} \
	--with-gnome --without-debug --sysconfdir=%{_sysconfdir}
else
  CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%{_prefix} \
	--with-gnome --without-debug --sysconfdir=%{_sysconfdir}
fi

if [ "$SMP" != "" ]; then
  (make "MAKE=make -k -j $SMP"; exit 0)
  make
else
  make
fi

%install
rm -rf $RPM_BUILD_ROOT

%{__make} prefix=$RPM_BUILD_ROOT%{_prefix} sysconfdir=$RPM_BUILD_ROOT%{_sysconfdir} install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)

%doc AUTHORS COPYING ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%{_datadir}/*
