Name:           cmocka
Version:        1.1.5
Release:        4

License:        ASL 2.0
Summary:        An elegant unit testing framework for C with support for mock objects
URL:            https://cmocka.org

Source0:        https://cmocka.org/files/1.1/%{name}-%{version}.tar.xz

BuildRequires:  cmake doxygen glibc-devel gnupg2 gcc

%description
Cmocka is an elegant unit testing framework for C with support for mock objects. 
It only requires the standard C library, works on a range of computing platforms 
(including embedded) and with different compilers.
This package is a library to simplify and generalize unit tests for C with 
support for mock objects 

%package -n libcmocka
Summary:        Lightweight library to simplify and generalize unit tests for C

Conflicts: cmockery2

%description -n libcmocka
Cmocka is an elegant unit testing framework for C with support for mock objects.
It only requires the standard C library, works on a range of computing platforms
(including embedded) and with different compilers.
This package is a library to simplify and generalize unit tests for C with
support for mock objects

%package -n    libcmocka-devel
Summary:       Development headers for the cmocka library
Requires:      libcmocka = %{version}-%{release}
Provides:      libcmocka-static = %{version}-%{release}
Obsoletes:     libcmocka-static < %{version}-%{release}
Conflicts:     cmockery2-devel

%description -n libcmocka-devel
Development headers for the cmocka unit testing library.

%prep
%autosetup -p1

%build
%if "%toolchain" == "clang"
	export CFLAGS="$CFLAGS -O0"
	export CXXFLAGS="$CXXFLAGS -O0"
%endif
if test ! -e "obj"; then
  mkdir obj
fi
cd obj/
%cmake \
  -DWITH_STATIC_LIB=ON \
  -DWITH_CMOCKERY_SUPPORT=ON \
  -DUNIT_TESTING=ON \
  %{_builddir}/%{name}-%{version}

%make_build VERBOSE=1
make docs
cd ../

%install
cd obj/
%make_install
cd ../
ln -s libcmocka.so %{buildroot}%{_libdir}/libcmockery.so

%post -n libcmocka -p /sbin/ldconfig

%postun -n libcmocka -p /sbin/ldconfig

%check
cd obj/
ctest --output-on-failure
cd ../

%files -n libcmocka
%doc COPYING  AUTHORS README.md ChangeLog
%{_libdir}/libcmocka.so.*

%files -n libcmocka-devel
%doc obj/doc/html
%{_includedir}/cmocka.h
%{_includedir}/cmocka_pbc.h
%{_includedir}/cmockery/cmockery.h
%{_includedir}/cmockery/pbc.h
%{_libdir}/libcmocka.so
%{_libdir}/libcmockery.so
%{_libdir}/pkgconfig/cmocka.pc
%{_libdir}/cmake/cmocka/cmocka-config-version.cmake
%{_libdir}/cmake/cmocka/cmocka-config.cmake
%{_libdir}/libcmocka-static.a

%changelog
* Tue Jun 27 2023 yoo <sunyuechi@iscas.ac.cn> - 1.1.5-4
- fix clang build error

* Mon May 31 2021 baizhonggui <baizhonggui@huawei.com> - 1.1.5-3
- Add gcc in BuildRequires

* Fri Jan 10 2020 chenli <chenli147@huawei.com> - 1.1.5-2
- Update version.

* Fri Nov 22 2019 Wanjiankang <wanjiankang@huawei.com> - 1.1.3-2
- Initial package.
