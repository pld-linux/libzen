Summary:	ZenLib C++ utility library
Summary(pl.UTF-8):	ZenLib - biblioteka narzędziowa C++
Name:		libzen
Version:	0.4.28
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://downloads.sourceforge.net/zenlib/%{name}_%{version}.tar.bz2
# Source0-md5:	f09e519b71e61a7226ffefe55d00eadf
Patch0:		%{name}-include.patch
URL:		http://sourceforge.net/projects/zenlib/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.11
BuildRequires:	doxygen
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	rpmbuild(macros) >= 1.566
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ZenLib is a C++ utility library. It includes classes for handling
strings, configuration, bit streams, threading, translation, and
cross-platform operating system functions.

%description -l pl.UTF-8
ZenLib to biblioteka narzędziowa C++. Zawiera klasy do obsługi
łańcuchów znaków, konfiguracji, strumieni bitowych, wątków,
tłumaczeń oraz wieloplatformowe funkcji dotyczące systemu
operacyjnego.

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

%prep
%setup -q -n ZenLib
%undos Source/ZenLib/*.h
%undos *.txt Source/Doc/*.html
chmod 644 *.txt Source/Doc/*.html
%patch0 -p1

%build
#export CFLAGS="%{rpmcflags}"
#export CPPFLAGS="%{rpmcppflags}"
#export CXXFLAGS="%{rpmcxxflags}"

cd Project/GNU/Library
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--enable-shared
%{__make} clean
%{__make}
cd ../../../Source/Doc
doxygen Doxyfile

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C Project/GNU/Library install \
	DESTDIR=$RPM_BUILD_ROOT

# Zenlib headers and ZenLib-config
install -d $RPM_BUILD_ROOT%{_includedir}/ZenLib
cp -a Source/ZenLib/*.h $RPM_BUILD_ROOT%{_includedir}/ZenLib

for i in HTTP_Client Format/Html Format/Http; do
	install -d $RPM_BUILD_ROOT%{_includedir}/ZenLib/$i
	cp -a Source/ZenLib/$i/*.h $RPM_BUILD_ROOT%{_includedir}/ZenLib/$i
done

%{__sed} -i -e 's|Version: .*|Version: %{version}|g' Project/GNU/Library/libzen.pc

install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
cp -a Project/GNU/Library/libzen.pc $RPM_BUILD_ROOT%{_pkgconfigdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc History.txt License.txt ReadMe.txt
%attr(755,root,root) %{_libdir}/libzen.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libzen.so.0

%files devel
%defattr(644,root,root,755)
# Documentation.html expects Doc/index.html
%doc Source/Doc/Documentation.html Doc
%attr(755,root,root) %{_bindir}/libzen-config
%attr(755,root,root) %{_libdir}/libzen.so
%{_libdir}/libzen.la
%{_includedir}/ZenLib
%{_pkgconfigdir}/libzen.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libzen.a
