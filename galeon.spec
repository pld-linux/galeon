Summary:	Galeon - gecko-based GNOME web browser
Summary(pl):	Galeon - przegl±darka WWW dla GNOME
Name:		galeon
Version:	0.11.0
Release:	1
License:	GPL
Group:		X11/Applications/Networking
Group(de):	X11/Applikationen/Netzwerkwesen
Group(pl):	X11/Aplikacje/Sieciowe
Source0:	http://prdownloads.sourceforge.net/galeon/%{name}-%{version}.tar.gz     	
Patch0:		%{name}-mozilla_five_home.patch
Patch1:		%{name}-macros.patch
Patch2:		%{name}-gettext.patch
URL:		http://galeon.sourceforge.net/
Requires:	mozilla >= 0.9.1
BuildRequires:	GConf-devel
BuildRequires:	ORBit-devel >= 0.5.0
BuildRequires:	gettext-devel
BuildRequires:	gnome-libs-devel >= 1.2.0
BuildRequires:	gnome-vfs-devel >= 0.5
BuildRequires:	libxml-devel >= 1.8.7
BuildRequires:	libglade-devel
BuildRequires:	libstdc++-devel
BuildRequires:	mozilla-devel >= 0.9.2
BuildRequires:	oaf >= 0.6.2
BuildRequires:	bison
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
Gnome browser based on Gecko (Mozilla rendering engine).

%description -l pl
Galeon jest przegl±dark± WWW bazuj±c± na Gecko (mechanizmie
interpretacji stron Mozilli).

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
rm missing
gettextize --copy --force
libtoolize --copy --force
aclocal
autoconf
automake -a -c
%configure \
	--with-mozilla-libs=%{_libdir} \
	--with-mozilla-includes=%{_includedir}/mozilla \
	--with-mozilla-home=%{_libdir}/mozilla \
	--enable-nls \
	--disable-included-gettext

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	Networkdir=%{_applnkdir}/Network/WWW

mv -f $RPM_BUILD_ROOT%{_bindir}/galeon-bin $RPM_BUILD_ROOT%{_bindir}/galeon

gzip -9nf AUTHORS ChangeLog NEWS README

%find_lang %{name} --with-gnome

%post
umask 022
rm -f %{_libdir}/mozilla/component.reg
MOZILLA_FIVE_HOME=%{_libdir}/mozilla regxpcom

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_bindir}/*
%{_applnkdir}/Network/WWW/*
%{_datadir}/galeon
%{_datadir}/oaf/*
%{_datadir}/sounds/galeon
%{_pixmapsdir}/*
