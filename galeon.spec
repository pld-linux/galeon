Summary:	Galeon - gecko-based GNOME web browser
Summary(pl):	Galeon - przegl±darka WWW
Name:		galeon
Version:	0.8
Release:	1
License:	GPL
Group:		X11/Applications/Networking
Group(de):	X11/Applikationen/Netzwerkwesen
Group(pl):	X11/Aplikacje/Sieciowe
Source0:	ftp://download.sourceforge.net/pub/sourceforge/galeon/%{name}-%{version}.tar.gz
Patch0:		%{name}-makefile.patch
URL:		http://galeon.sourceforge.net/
Requires:	mozilla
BuildRequires:	ORBit-devel >= 0.5.0
BuildRequires:	gettext-devel
BuildRequires:	gnome-libs-devel >= 1.2.0
BuildRequires:	libxml-devel >= 1.8.7
BuildRequires:	libglade-devel
BuildRequires:	libstdc++-devel
BuildRequires:	mozilla-devel
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

%build
gettextize --copy --force
%configure \
	--with-gnome \
	--without-debug \
	--enable-gcc-compatibility-hack
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

gzip -9nf AUTHORS ChangeLog NEWS README

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_bindir}/*
%{_applnkdir}/Network/WWW/*
%{_datadir}/galeon
%{_datadir}/pixmaps/*
