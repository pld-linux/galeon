
%define		minmozver	1.1
%define		snap		20020929

Summary:	Galeon - gecko-based GNOME web browser
Summary(pl):	Galeon - przegl±darka WWW dla GNOME
Summary(pt_BR):	O galeon é um browser para o gnome baseado no mozilla
Summary(zh_CN):	»ùÓÚGeckoµÄGNOMEÁ÷ÀÀÆ÷
Name:		galeon
Version:	1.2.99
Release:	0.%{snap}
Epoch:		2
License:	GPL
Group:		X11/Applications/Networking
#Source0:	http://unc.dl.sourceforge.net/sourceforge/galeon/%{name}-%{version}.tar.gz
Source0:	%{name}-%{version}.%{snap}.tar.bz2
Source1:	%{name}-config-tool.1
URL:		http://galeon.sourceforge.net/
BuildRequires:	GConf2-devel
BuildRequires:	ORBit2-devel
BuildRequires:	bison
BuildRequires:	bonobo-activation-devel
BuildRequires:	gettext-devel
BuildRequires:	gnome-vfs2-devel
BuildRequires:	gtk+2-devel >= 2.0.6
BuildRequires:	intltool
BuildRequires:	libglade2-devel
BuildRequires:	libgnomeui-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libxml2-devel
BuildRequires:	mozilla-embedded-devel >= %{minmozver}
#BuildRequires:	nautilus-devel >= 2.0.0
BuildRequires:	openssl-devel
BuildRequires:	scrollkeeper
Requires:	mozilla-embedded = %(rpm -q --qf '%{VERSION}' --whatprovides mozilla-embedded)
Prereq:		scrollkeeper
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# can be provided by mozilla or mozilla-embedded
%define		_noautoreqdep	libgtkembedmoz.so libgtksuperwin.so libxpcom.so

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man
%define		_sysconfdir	/etc/X11/GNOME2
%define         _omf_dest_dir   %(scrollkeeper-config --omfdir)
%define		_gcc_ver	%(%{__cc} -dumpversion | cut -b 1)

%description
Gnome browser based on Gecko (Mozilla rendering engine).

%description -l pl
Galeon jest przegl±dark± WWW bazuj±c± na Gecko (mechanizmie
interpretacji stron Mozilli).

%description -l pt_BR
O galeon é um browser para o gnome baseado no mozilla.

%prep
%setup -q

%build
rm -f missing
glib-gettextize --copy --force
xml-i18n-toolize --copy --force
libtoolize --copy --force
aclocal -I %{_aclocaldir}/gnome2-macros
autoheader
%{__autoconf}
%{__automake}
#%if %{_gcc_ver} > 2
#CXXFLAGS="-Wno-deprecated"; export CXXFLAGS
#%endif
%configure \
	--with-mozilla-libs=%{_libdir} \
	--with-mozilla-includes=%{_includedir}/mozilla \
	--with-mozilla-home=%{_libdir}/mozilla \
	--enable-nls \
	--disable-included-gettext \
	--disable-install-schemas \
	--disable-werror \
	--enable-gconf-source=%{_sysconfdir}/gconf/schemas \
	--enable-nautilus-view=yes

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}/man1

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	Networkdir=%{_applnkdir}/Network/WWW \
	omf_dest_dir=%{_omf_dest_dir}/%{name}

#mv -f $RPM_BUILD_ROOT%{_bindir}/galeon-bin $RPM_BUILD_ROOT%{_bindir}/galeon

install %{SOURCE1} $RPM_BUILD_ROOT%{_mandir}/man1

%find_lang %{name} --with-gnome

%post
/usr/bin/scrollkeeper-update
umask 022
rm -f %{_libdir}/mozilla/component.reg
MOZILLA_FIVE_HOME=%{_libdir}/mozilla regxpcom
GCONF_CONFIG_SOURCE="" gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/galeon.schemas >/dev/null

%postun -p /usr/bin/scrollkeeper-update

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
#%{_applnkdir}/Network/WWW/*
%{_libdir}/%{name}
%{_libdir}/bonobo/servers/*
%{_datadir}/galeon
%{_datadir}/applications/*
%{_datadir}/gnome/help/galeon-manual
%{_datadir}/gnome-2.0/ui/*.xml
%{_omf_dest_dir}/%{name}
%{_datadir}/sounds/galeon
%{_pixmapsdir}/*
%{_sysconfdir}/gconf/schemas/*
%{_sysconfdir}/sound/events/*
%{_mandir}/man1/*
