
%define		minmozver	1.2.1

Summary:	Galeon - gecko-based GNOME web browser
Summary(pl):	Galeon - przegl±darka WWW dla GNOME
Summary(pt_BR):	O galeon é um browser para o gnome baseado no mozilla
Summary(zh_CN):	»ùÓÚGeckoµÄGNOMEÁ÷ÀÀÆ÷
Name:		galeon
Version:	1.2.7
Release:	4
Epoch:		2
License:	GPL
Group:		X11/Applications/Networking
Source0:	http://dl.sourceforge.net/sourceforge/galeon/%{name}-%{version}.tar.gz
# Source0-md5:	2408b7e6b1a2a2655f6720b41a391f4b
Source1:	%{name}-config-tool.1
Patch0:		%{name}-mozilla_five_home.patch
Patch1:		%{name}-am_fix.patch
Patch2:		%{name}-omf.patch
Patch3:		%{name}-pl.patch
Patch4:		%{name}-notypeaheadfindin1.0.patch
URL:		http://galeon.sourceforge.net/
BuildRequires:	GConf-devel >= 1.0.9-2
BuildRequires:	ORBit-devel >= 0.5.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	gdk-pixbuf-devel >= 0.10.
BuildRequires:	gettext-devel
BuildRequires:	gnome-core-devel >= 1.2.0
BuildRequires:	gnome-libs-devel >= 1.2.0
BuildRequires:	gnome-vfs-devel >= 0.5
BuildRequires:	intltool
BuildRequires:	libglade-gnome-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libxml-devel >= 1.8.7
BuildRequires:	mozilla-embedded-devel >= %{minmozver}
BuildRequires:	oaf-devel >= 0.6.2
BuildRequires:	openssl-devel >= 0.9.6m
BuildRequires:	scrollkeeper
Requires:	GConf >= 1.0.4-1
Requires:	mozilla-embedded = %(rpm -q --qf '%{VERSION}' --whatprovides mozilla-embedded)
Requires(post):	GConf
Requires(post):	mozilla
Requires(post):	scrollkeeper
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# can be provided by mozilla or mozilla-embedded
%define		_noautoreqdep	libgtkembedmoz.so libgtksuperwin.so libxpcom.so

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man
%define		_sysconfdir	/etc/X11/GNOME
%define         _omf_dest_dir   %(scrollkeeper-config --omfdir)

# supports 1.0, 1.1, 1.2 or trunk (1.3)
%define	mozsnap	%(rpm -q --qf '%{VERSION}' --whatprovides mozilla-embedded | sed -e 's/^\([0-9]\.[0-9]\).*/\1/;s/^1\.3$/trunk/')

%description
Gnome browser based on Gecko (Mozilla rendering engine).

%description -l pl
Galeon jest przegl±dark± WWW bazuj±c± na Gecko (mechanizmie
interpretacji stron Mozilli).

%description -l pt_BR
O galeon é um browser para o gnome baseado no mozilla.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
rm -f missing
xml-i18n-toolize --copy --force
%{__gettextize}
%{__aclocal} -I %{_aclocaldir}/gnome
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--with-mozilla-libs=%{_libdir} \
	--with-mozilla-includes=%{_includedir}/mozilla \
	--with-mozilla-home=%{_libdir}/mozilla \
	--enable-nls \
	--disable-included-gettext \
	--disable-install-schemas \
	--disable-werror \
	--with-mozilla-snapshot=1.2 \
	--enable-gconf-source=%{_sysconfdir}/gconf/schemas \
	--enable-nautilus-view=no

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}/man1

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	Networkdir=%{_applnkdir}/Network/WWW \
	omf_dest_dir=%{_omf_dest_dir}/%{name}

mv -f $RPM_BUILD_ROOT%{_bindir}/galeon-bin $RPM_BUILD_ROOT%{_bindir}/galeon

install %{SOURCE1} $RPM_BUILD_ROOT%{_mandir}/man1

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/bin/scrollkeeper-update
umask 022
rm -f %{_libdir}/mozilla/{component.reg,components/{compreg,xpti}.dat}
MOZILLA_FIVE_HOME=%{_libdir}/mozilla regxpcom
gconftool --shutdown
GCONF_CONFIG_SOURCE=xml::%{_sysconfdir}/gconf/gconf.xml.defaults gconftool --makefile-install-rule %{_sysconfdir}/gconf/schemas/galeon.schemas 2>dev/null >/dev/null

%postun -p /usr/bin/scrollkeeper-update

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%{_applnkdir}/Network/WWW/*
%{_libdir}/%{name}
%{_datadir}/galeon
%{_datadir}/gnome/help/galeon-manual
%{_datadir}/gnome/ui/*.xml
%{_datadir}/oaf/*
%{_omf_dest_dir}/%{name}
%{_datadir}/sounds/galeon
%{_pixmapsdir}/*
%{_sysconfdir}/gconf/schemas/*
%{_sysconfdir}/sound/events/*
%{_mandir}/man1/*
