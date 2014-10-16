%define		ver	%(echo %{version} | tr . _)

Summary:	International Components for Unicode
Name:		icu
Version:	53.1
Release:	1
License:	X License
Group:		Libraries
Source0:	http://download.icu-project.org/files/icu4c/%{version}/%{name}4c-%{verZ}-src.tgz
# Source0-md5:	b73baa6fbdfef197608d1f69300919b9
Patch0:		%{name}-aclocal-hack.patch
URL:		http://www.ibm.com/software/globalization/icu/
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	libstdc++-devel
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ICU is a set of C and C++ libraries that provides robust and
full-featured Unicode and locale support. The library provides
calendar support, conversions for many character sets, language
sensitive collation, date and time formatting, support for many
locales, message catalogs and resources, message formatting,
normalization, number and currency formatting, time zones support,
transliteration, word, line and sentence breaking, etc.

This package contains the Unicode character database and derived
properties, along with converters and time zones data.

%package libs
Summary:	International Components for Unicode (libraries)
Group:		Development/Libraries

%description libs
ICU is a set of C and C++ libraries that provides robust and
full-featured Unicode support. This package contains the runtime
libraries for ICU. It does not contain any of the data files needed at
runtime and present in the `icu' and `icu-locales` packages.

%package devel
Summary:	International Components for Unicode (development files)
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
ICU is a set of C and C++ libraries that provides robust and
full-featured Unicode support. This package contains the development
files for ICU.

%prep
%setup -q -n %{name}
%patch0 -p1

%build
cd source
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%configure \
	--disable-samples	\
	--sbindir=%{_bindir}	\
	--with-data-packaging=library
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C source install \
	DESTDIR=$RPM_BUILD_ROOT

# help rpm to generate deps
chmod +x $RPM_BUILD_ROOT%{_libdir}/*

rm -f $RPM_BUILD_ROOT%{_datadir}/icu/%{version}/license.html

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc license.html readme.html
%attr(755,root,root) %{_bindir}/*
%exclude %{_bindir}/icu-config
%{_mandir}/man1/*
%{_mandir}/man8/*
%exclude %{_mandir}/man1/icu-config.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/lib*.so.??
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/icu-config
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_datadir}/%{name}/%{version}/install-sh
%attr(755,root,root) %{_datadir}/%{name}/%{version}/mkinstalldirs

%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/%{version}
%dir %{_includedir}/layout
%dir %{_includedir}/unicode
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{version}
%dir %{_libdir}/%{name}/current

%{_datadir}/%{name}/%{version}/config
%{_includedir}/layout/*.h
%{_includedir}/unicode/*.h
%{_libdir}/%{name}/%{version}/*.inc
%{_libdir}/%{name}/*.inc
%{_pkgconfigdir}/*.pc
%{_mandir}/man1/icu-config.1*

