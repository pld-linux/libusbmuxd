#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_without	tests		# build without tests

Summary:	Client library to communicate with the USB multiplex daemon for Apple's iOS devices
Summary(pl.UTF-8):	Biblioteka kliencka do komunikacji z demonem multipleksującym USB dla urządzeń z Apple iOS
Name:		libusbmuxd
Version:	1.0.10
Release:	4
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://www.libimobiledevice.org/downloads/%{name}-%{version}.tar.bz2
# Source0-md5:	e5351ff6f6eedcb50701e02d91cc480c
URL:		http://www.libimobiledevice.org/
BuildRequires:	libplist-devel >= 1.11
BuildRequires:	pkgconfig
Requires:	libplist >= 1.11
Obsoletes:	usbmuxd-libs < 1.0.9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%undefine	__cxx

%description
libusbmuxd is the client library used for communicating with Apple's
iPod Touch, iPhone, iPad and Apple TV devices. It allows multiple
services on the device to be accessed simultaneously.

%description -l pl.UTF-8
libusbmuxd to biblioteka kliencka służąca do komunikacji z
urządzeniami Apple iPod Touch, iPhone, iPad oraz Apple TV. Pozwala na
jednoczesny dostęp do wielu usług jednego urządzenia.

%package utils
Summary:	Utilities for communicating with Apple's iOS devices
Summary(pl.UTF-8):	Narzędzia do komunikacji z urządzeniami Apple iOS
License:	GPL v2+
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description utils
Utilities for communicating with Apple's iOS devices.

%description utils -l pl.UTF-8
Narzędzia do komunikacji z urządzeniami Apple iOS.

%package devel
Summary:	Header files for libusbmuxd
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libusbmuxd
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Provides:	usbmuxd-devel = %{version}-%{release}
Obsoletes:	usbmuxd-devel < 1.0.9

%description devel
Header files for libusbmuxd.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libusbmuxd.

%package static
Summary:	Static libusbmuxd library
Summary(pl.UTF-8):	Statyczna biblioteka libusbmuxd
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libusbmuxd library.

%description static -l pl.UTF-8
Statyczna biblioteka libusbmuxd.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}

%{__make}

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL='install -p' \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libusbmuxd.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%attr(755,root,root) %{_libdir}/libusbmuxd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libusbmuxd.so.4

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/iproxy

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libusbmuxd.so
%{_includedir}/usbmuxd.h
%{_includedir}/usbmuxd-proto.h
%{_pkgconfigdir}/libusbmuxd.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libusbmuxd.a
%endif
