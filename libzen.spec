Summary:	Shared library for libmediainfo and mediainfo*
Name:		libzen
Version:	0.4.12
Release:	1
License:	BSD
Group:		Libraries
URL:		http://mediainfo.sourceforge.net/
Source0:	http://downloads.sourceforge.net/project/zenlib/ZenLib%20-%20Sources/%{version}/%{name}_%{version}.tar.bz2
# Source0-md5:	9e63ff3d0fb51b6cd402de96e2b9bc65
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dos2unix
BuildRequires:	doxygen
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Shared library for libmediainfo and mediainfo-*.

%package -n libzen-devel
Summary:	Include files and mandatory libraries for development
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n libzen-devel
Include files and mandatory libraries for development.

%package static
Summary:	Static libzen library
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libzen library.

%prep
%setup -q -n ZenLib
dos2unix *.txt Source/Doc/*.html
chmod 644 *.txt Source/Doc/*.html

%build
export CFLAGS="%{rpmcflags}"
export CPPFLAGS="%{rpmcppflags}"
export CXXFLAGS="%{rpmcxxflags}"

cd Source/Doc
	doxygen Doxyfile
cd ../..

cp Source/Doc/*.html ./

cd Project/GNU/Library
	chmod +x autogen
	./autogen
	%configure \
	--enable-shared \

	%{__make} clean
	%{__make}
cd ../../..

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C Project/GNU/Library \
	install-strip \
	DESTDIR=$RPM_BUILD_ROOT

# Zenlib headers and ZenLib-config
install -d $RPM_BUILD_ROOT%{_includedir}/ZenLib
cp -a Source/ZenLib/*.h $RPM_BUILD_ROOT%{_includedir}/ZenLib

for i in Base64 HTTP_Client Format/Html Format/Http; do
	install -d $RPM_BUILD_ROOT%{_includedir}/ZenLib/$i
	cp -a Source/ZenLib/$i/*.h $RPM_BUILD_ROOT%{_includedir}/ZenLib/$i
done

%{__sed} -i -e 's|Version: |Version: %{version}|g' Project/GNU/Library/libzen.pc

install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
cp -a Project/GNU/Library/libzen.pc $RPM_BUILD_ROOT%{_pkgconfigdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc History.txt License.txt ReadMe.txt
%attr(755,root,root) %{_libdir}/libzen.so.*

%files devel
%defattr(644,root,root,755)
%doc Documentation.html
%doc Doc/*
%dir %{_includedir}/ZenLib
%{_includedir}/ZenLib/*
%{_libdir}/libzen.la
%attr(755,root,root) %{_libdir}/libzen.so
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libzen.a
