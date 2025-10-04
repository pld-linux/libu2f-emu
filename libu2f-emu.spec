#
# Conditional build:
%bcond_without	apidocs		# API documentation
#
Summary:	Universal 2nd Factor (U2F) Emulation C Library
Summary(pl.UTF-8):	Biblioteka C emulacji U2F (Universal 2nd Factor)
Name:		libu2f-emu
Version:	0
%define	gitref	d1c4b9c2e1c42e8931033912c8b609521f2a7756
%define	snap	20200905
Release:	0.%{snap}.1
License:	GPL v2
Group:		Libraries
#Source0Download: https://github.com/MattGorko/libu2f-emu/tags
Source0:	https://github.com/MattGorko/libu2f-emu/archive/%{gitref}/%{name}-%{snap}.tar.gz
# Source0-md5:	79aa3b26eaf704d530aa49d8430d306b
Patch0:		no-apidocs.patch
URL:		https://github.com/MattGorko/libu2f-emu
%{?with_apidocs:BuildRequires:	doxygen}
%{?with_apidocs:BuildRequires:	graphviz}
# for tests
BuildRequires:	gtest-devel >= 1.10.0
BuildRequires:	meson >= 0.52.0
BuildRequires:	ninja >= 1.5
BuildRequires:	openssl-devel >= 1.1.0
BuildRequires:	openssl-tools >= 1.1.0
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libu2f-emu provides a C Library for the U2F device emulations.

%description -l pl.UTF-8
Ten pakiet dostarcza bibliotekę C do emulacji urządzeń U2F.

%package devel
Summary:	Header files for u2f-emu library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki u2f-emu
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for u2f-emu library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki u2f-emu.

%package apidocs
Summary:	API documentation for u2f-emu library
Summary(pl.UTF-8):	Dokumentacja API biblioteki u2f-emu
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for u2f-emu library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki u2f-emu.

%prep
%setup -q -n %{name}-%{gitref}
%patch -P0 -p1

# allow build without -devel already installed
ln -sf ../src/u2f-emu{,-types}.h tests

# as of 2020 it uses APIs deprecated in openssl 3
%{__sed} -i -e '/werror=true/d' meson.build

# gtest 1.15 requires C++14
%{__sed} -i -e 's/cpp_std=c++11/cpp_std=c++14/' meson.build

%build
%meson

%meson_build

%if %{with apidocs}
%meson_build doc
%endif

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libu2f-emu.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libu2f-emu.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libu2f-emu.so
%{_includedir}/u2f-emu*.h
%{_pkgconfigdir}/u2f-emu.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/doc/html/{search,*.{css,html,js,png}}
%endif
