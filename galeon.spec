
Summary:	Galeon
Summary(pl):    Galeon - przegl±darka WWW
Name:		galeon
Version:	0.7.6
Release:	1
License:	GPL
Group:		X11/Applications/Networking
Group(pl):	X11/Aplikacje/Sieciowe
Source0:	ftp://download.sourceforge.net/pub/sourceforge/galeon/%{name}-%{version}.tar.gz
URL:		http://galeon.sourceforge.net/
Patch0:         %{name}-makefile.patch
Requires:	mozilla
Requires:	gnome-libs >= 1.0.0
Requires:	ORBit >= 0.4.0
BuildRequires:	libxml-devel >= 1.8.7
BuildRequires:	mozilla-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)


%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
Gnome browser based on Gecko (Mozilla rendering engine).

%description -l pl
Galeon jest przegl±dark± WWW bazuj±c± na Gecko (mechani¼mie interpretacji stron Mozilli)

%prep
%setup -q
%patch0 -p1

%build
gettextize -c -f
LDFLAGS="-s"; export LDFLAGS
%configure \
	--with-gnome \
	--without-debug \
	--enable-gcc-compatibility-hack
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

gzip -9nf AUTHORS ChangeLog NEWS README

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_bindir}/*
%{_datadir}/*
