#
# Conditional build:
%bcond_without nautilus	# disable nautilus view
%bcond_with gcc2	# compile using gcc2 to get working gcc2-compiled java
			# plugin (better get gcc3-compiled one).
			# Flash plugin seems to still not work, use
			# mozilla instead. To compile wit this option, You
			# have to install mozilla compiled with gcc2.
#
%define		minmozver	5:1.6
%define		snap	20040117

Summary:	Galeon - gecko-based GNOME web browser
Summary(pl):	Galeon - przegl±darka WWW dla GNOME
Summary(pt_BR):	O galeon é um browser para o GNOME baseado no mozilla
Summary(zh_CN):	»ùÓÚGeckoµÄGNOMEÁ÷ÀÀÆ÷
Name:		galeon
Version:	1.3.13a
Release:	1
Epoch:		2
License:	GPL
Group:		X11/Applications/Networking
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
# Source0-md5:	c29bdfb23fdafddfcfb6ae7fc6c822fd
#Source0:	%{name}-%{version}-%{snap}.tar.bz2
Source1:	%{name}-config-tool.1
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-home_etc.patch
Patch2:		%{name}-locale-names.patch
URL:		http://galeon.sourceforge.net/
BuildRequires:	GConf2-devel >= 2.4.0
BuildRequires:	ORBit2-devel >= 2.8.3
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	gettext-devel
BuildRequires:	gnome-vfs2-devel >= 2.4.0
BuildRequires:	gtk+2-devel >= 2.2.0
BuildRequires:	intltool
BuildRequires:	libbonoboui-devel >= 2.4.0
BuildRequires:	libglade2-devel >= 2.0.1
BuildRequires:	libgnomeui-devel >= 2.4.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 2.4.0
BuildRequires:	mozilla-devel >= %{minmozver}
%{?with_nautilus:BuildRequires:	nautilus-devel >= 2.4.0}
BuildRequires:	openssl-devel >= 0.9.7c
BuildRequires:	rpm-build >= 4.1-10
BuildRequires:	scrollkeeper >= 0.1.4
Requires(post):	GConf2
Requires(post):	scrollkeeper
Requires:	libbonobo >= 2.4.0
Requires:	mozilla = %(rpm -q --qf '%{EPOCH}:%{VERSION}' --whatprovides mozilla)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# can be provided by mozilla or mozilla-embedded
%define		_noautoreqdep	libgtkembedmoz.so libgtksuperwin.so libxpcom.so

%if %{with gcc2}
%define         __cc            gcc2
%define         __cxx           gcc2
%endif

%description
GNOME browser based on Gecko (Mozilla rendering engine).

%description -l pl
Galeon jest przegl±dark± WWW bazuj±c± na Gecko (mechanizmie
interpretacji stron Mozilli).

%description -l pt_BR
O galeon é um browser para o GNOME baseado no mozilla.

%prep
%setup -q -n %{name}-1.3.13
%patch0 -p1
%patch1 -p1
%patch2 -p1

mv po/{no,nb}.po

# regenerate - didn't compile with ORBit2 2.7.2
cd idl
orbit-idl-2 -I /usr/share/idl/bonobo-2.0 -I /usr/share/idl/bonobo-activation-2.0 Galeon*.idl
mv Galeon*.[ch] ../src

%build
rm -f missing
glib-gettextize --copy --force
intltoolize --copy --force
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--disable-schemas-install \
	%if %{with nautilus}
	--enable-nautilus-view=yes
	%else
	--enable-nautilus-view=no
	%endif
	

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}/man1

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_mandir}/man1

rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/components/*.la

# galeon-2.0.mo, but gnome/help/galeon
%find_lang galeon-2.0 --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/bin/scrollkeeper-update
%gconf_schema_install

%postun -p /usr/bin/scrollkeeper-update

%files -f galeon-2.0.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/%{name}
%{_libdir}/bonobo/servers/*
%{_datadir}/galeon
%{_desktopdir}/*
%{_datadir}/gnome-2.0/ui/*.xml
%{_omf_dest_dir}/%{name}
%{_datadir}/sounds/galeon
%{_pixmapsdir}/*
%{_sysconfdir}/gconf/schemas/*
%{_sysconfdir}/sound/events/*
%{_mandir}/man1/*
