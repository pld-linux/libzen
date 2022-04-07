#
# Conditional build:
%bcond_without	apidocs		# API documentation (doxygen generated)
%bcond_without	static_libs	# static library

Summary:	ZenLib C++ utility library
Summary(pl.UTF-8):	ZenLib - biblioteka narzędziowa C++
Name:		libzen
Version:	0.4.39
Release:	1
License:	BSD
Group:		Libraries
Source0:	https://mediaarea.net/download/source/libzen/%{version}/%{name}_%{version}.tar.xz
# Source0-md5:	61c47005f2d383876b0bce57ee173e20
Patch0:		%{name}-include.patch
URL:		https://github.com/MediaArea/ZenLib
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.11
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	rpmbuild(macros) >= 1.566
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ZenLib is a C++ utility library. It includes classes for handling
strings, configuration, bit streams, threading, translation, and
cross-platform operating system functions.

%description -l pl.UTF-8
ZenLib to biblioteka narzędziowa C++. Zawiera klasy do obsługi
łańcuchów znaków, konfiguracji, strumieni bitowych, wątków, tłumaczeń
oraz wieloplatformowe funkcji dotyczące systemu operacyjnego.

%package devel
Summary:	Header files for ZenLib library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ZenLib
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for ZenLib library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki ZenLib.

%package static
Summary:	Static ZenLib library
Summary(pl.UTF-8):	Statyczna biblioteka ZenLib
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ZenLib library.

%description static -l pl.UTF-8
Statyczna biblioteka ZenLib.

%package apidocs
Summary:	API documentation for ZenLib library
Summary(pl.UTF-8):	Dokumentacja API biblioteki ZenLib
Group:		Documentation

%description apidocs
API documentation for ZenLib library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki ZenLib.

%prep
%setup -q -n ZenLib
%undos Source/ZenLib/*.h
%undos *.txt Source/Doc/*.html
chmod 644 *.txt Source/Doc/*.html
%patch0 -p1

%build
cd Project/GNU/Library
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	%{?with_static_libs:--enable-static}
%{__make} clean
%{__make}

%if %{with apidocs}
cd ../../../Source/Doc
doxygen Doxyfile
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C Project/GNU/Library install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libzen.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc History.txt License.txt README.md
%attr(755,root,root) %{_libdir}/libzen.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libzen.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libzen.so
%{_includedir}/ZenLib
%{_pkgconfigdir}/libzen.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libzen.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
# Documentation.html expects Doc/index.html
%doc Source/Doc/Documentation.html Doc
%endif
