#
# Conditional build:
# _with_gcc2		- compile using gcc2 to get working java plugin.
#			  Flash plugin seems to still doesn't work, use 
#			  mozilla instead. To compile wit this option, You 
#			  have to install mozilla compiled with gcc2.
#
%define		minmozver	1.4b
%define		snap		20030518

Summary:	Galeon - gecko-based GNOME web browser
Summary(pl):	Galeon - przegl�darka WWW dla GNOME
Summary(pt_BR):	O galeon � um browser para o gnome baseado no mozilla
Summary(zh_CN):	����Gecko��GNOME������
Name:		galeon
Version:	1.3.5
#Release:	1.%{snap}.1
Release:	1
Epoch:		2
License:	GPL
Group:		X11/Applications/Networking
Source0:	http://dl.sf.net/galeon/%{name}-%{version}.tar.bz2
# Source0-md5:	6d0a503e82e0c676712859ee273dcd81
#Source0:	%{name}-%{version}-%{snap}.tar.bz2
Source1:	%{name}-config-tool.1
URL:		http://galeon.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	GConf2-devel >= 2.0.0
BuildRequires:	ORBit2-devel >= 2.0.0
BuildRequires:	bison
BuildRequires:	gettext-devel
BuildRequires:	gnome-vfs2-devel >= 2.0.0
BuildRequires:	gtk+2-devel >= 2.0.6
BuildRequires:	intltool
BuildRequires:	libbonobo-devel >= 2.3.1-4
BuildRequires:	libbonoboui-devel >= 2.1.1
BuildRequires:	libglade2-devel >= 2.0.0
BuildRequires:	libgnomeui-devel >= 2.0.5
BuildRequires:	libstdc++-devel
BuildRequires:	libxml2-devel >= 2.4.0
BuildRequires:	mozilla-embedded-devel >= %{minmozver}
BuildRequires:	nautilus-devel >= 2.0.0
BuildRequires:	openssl-devel >= 0.9.7
BuildRequires:	scrollkeeper >= 0.1.4
BuildRequires:	rpm-build >= 4.1-10
Requires:	libbonobo >= 2.3.1-4
Requires:	mozilla-embedded = %(rpm -q --qf '%{VERSION}' --whatprovides mozilla-embedded)
Requires(post):	GConf2
Requires(post):	mozilla
Requires(post):	scrollkeeper
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# can be provided by mozilla or mozilla-embedded
%define		_noautoreqdep	libgtkembedmoz.so libgtksuperwin.so libxpcom.so

%if%{?_with_gcc2:1}%{!?_with_gcc2:0}
%define         __cc            gcc2
%define         __cxx           gcc2
%endif

%description
Gnome browser based on Gecko (Mozilla rendering engine).

%description -l pl
Galeon jest przegl�dark� WWW bazuj�c� na Gecko (mechanizmie
interpretacji stron Mozilli).

%description -l pt_BR
O galeon � um browser para o gnome baseado no mozilla.

%prep
%setup -q

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
	--with-mozilla-libs=%{_libdir} \
	--with-mozilla-includes=%{_includedir}/mozilla \
	--with-mozilla-home=%{_libdir}/mozilla \
	--enable-nls \
	--disable-included-gettext \
	--disable-schemas-install \
	--disable-werror \
	--with-mozilla-snapshot=1.4b \
	--enable-gconf-source=%{_sysconfdir}/gconf/schemas \
	--enable-nautilus-view=yes

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}/man1

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT 

install %{SOURCE1} $RPM_BUILD_ROOT%{_mandir}/man1

%find_lang galeon-2.0

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/bin/scrollkeeper-update
umask 022
rm -f %{_libdir}/mozilla/component.reg
MOZILLA_FIVE_HOME=%{_libdir}/mozilla regxpcom
%gconf_schema_install

%postun -p /usr/bin/scrollkeeper-update

%files -f galeon-2.0.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README*
%attr(755,root,root) %{_bindir}/*
%{_libdir}/%{name}
%{_libdir}/bonobo/servers/*
%{_datadir}/galeon
%{_datadir}/applications/*
%{_datadir}/gnome/help/*
%{_datadir}/gnome-2.0/ui/*.xml
%{_omf_dest_dir}/%{name}
%{_datadir}/sounds/galeon
%{_pixmapsdir}/*
%{_sysconfdir}/gconf/schemas/*
%{_sysconfdir}/sound/events/*
%{_mandir}/man1/*
