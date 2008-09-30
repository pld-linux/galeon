#
# TODO:
#   - force galeon to use old SSL dialogs using nsIBadCertListener, ie. port
#     EphyBadCertRejector from Epiphany, this will fix issues with https sites
#     using self signed and expired certificates or mismatches in domain names
#
# Conditional build:
%bcond_with	nautilus	# enable nautilus view
%bcond_with	gcc2		# compile using gcc2 to get working gcc2-compiled java
				# plugin (better get gcc3-compiled one).
				# Flash plugin seems to still not work, use
				# mozilla instead. To compile wit this option, You
				# have to install mozilla compiled with gcc2.
#
Summary:	Galeon - gecko-based GNOME web browser
Summary(pl.UTF-8):	Galeon - przeglądarka WWW dla GNOME
Summary(pt_BR.UTF-8):	O galeon é um browser para o GNOME baseado no mozilla
Summary(zh_CN.UTF-8):	基于Gecko的GNOME流览器
Name:		galeon
Version:	2.0.7
Release:	1
Epoch:		2
License:	GPL
Group:		X11/Applications/Networking
Source0:	http://dl.sourceforge.net/galeon/%{name}-%{version}.tar.bz2
# Source0-md5:	2eede1f43e3f6f2ac4ce7d4db99b15b2
Source1:	%{name}-config-tool.1
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-home_etc.patch
Patch2:		%{name}-ti-agent.patch
Patch3:		%{name}-agent.patch
Patch4:		%{name}-libxul.patch
Patch5:		%{name}-xul_includes_fix.patch
URL:		http://galeon.sourceforge.net/
BuildRequires:	GConf2-devel >= 2.4.0
BuildRequires:	ORBit2-devel >= 2.8.3
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.4.4
BuildRequires:	gnome-desktop-devel >= 2.9.91
BuildRequires:	gnome-vfs2-devel >= 2.10.0-2
BuildRequires:	gtk+2-devel >= 2:2.4.4
BuildRequires:	intltool
BuildRequires:	libbonoboui-devel >= 2.4.0
BuildRequires:	libglade2-devel >= 1:2.4.0
BuildRequires:	libgnomeui-devel >= 2.6.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 2.6.6
BuildRequires:	xulrunner-devel >= 1.8.0.4
%{?with_nautilus:BuildRequires:	nautilus-devel >= 2.4.0}
BuildRequires:	pkgconfig
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	scrollkeeper >= 0.1.4
BuildRequires:	sed >= 4.0
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	scrollkeeper
Requires(post,preun):	GConf2
Requires:	glib2 >= 1:2.4.4
Requires:	gtk+2 >= 2:2.4.4
Requires:	libbonobo >= 2.4.0
%requires_eq_to	xulrunner xulrunner-devel
Provides:	wwwbrowser
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# can be provided by mozilla or mozilla-embedded
%define		_noautoreqdep	libgtkembedmoz.so libgtksuperwin.so libxpcom.so
# we have strict deps for it
%define		_noautoreq	libxpcom.so

%if %{with gcc2}
%define		__cc		gcc2
%define		__cxx		gcc2
%endif

%description
GNOME browser based on Gecko (Mozilla rendering engine).

%description -l pl.UTF-8
Galeon jest przeglądarką WWW bazującą na Gecko (mechanizmie
interpretacji stron Mozilli).

%description -l pt_BR.UTF-8
O galeon é um browser para o GNOME baseado no mozilla.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%if "%{pld_release}" == "ti"
%patch2 -p1
%else
%patch3 -p1
%endif
%patch4 -p1
%patch5 -p1

sed -i -e 's#sr\@Latn#sr\@latin#' configure.in
mv po/sr\@{Latn,latin}.po

# regenerate - didn't compile with ORBit2 2.7.2
cd idl
orbit-idl-2 -I /usr/share/idl/bonobo-2.0 -I /usr/share/idl/bonobo-activation-2.0 Galeon*.idl
mv Galeon*.[ch] ../src

%build
cp /usr/share/automake/mkinstalldirs .
%{__glib_gettextize}
%{__intltoolize}
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

# No components installed now.
#rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/components/*.la

# galeon-2.0.mo, but gnome/help/galeon
%find_lang galeon-2.0 --with-gnome --with-omf --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%scrollkeeper_update_post
%gconf_schema_install galeon.schemas
%update_desktop_database_post

%preun
%gconf_schema_uninstall galeon.schemas

%postun
%scrollkeeper_update_postun
%update_desktop_database_postun

%files -f galeon-2.0.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README*
%attr(755,root,root) %{_bindir}/*
%{_libdir}/bonobo/servers/*
%{_datadir}/galeon
%{_desktopdir}/*.desktop
%{_datadir}/gnome-2.0/ui/*.xml
%{_datadir}/sounds/galeon
%{_pixmapsdir}/*
%{_sysconfdir}/gconf/schemas/galeon.schemas
%{_sysconfdir}/sound/events/*
%{_mandir}/man1/*
