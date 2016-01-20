#
# Conditional build:
%bcond_without	tests		# build without tests

Summary:	Client library USB multiplex daemon for Apple's iOS devices
Name:		libusbmuxd
Version:	1.0.10
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://www.libimobiledevice.org/downloads/%{name}-%{version}.tar.bz2
# Source0-md5:	e5351ff6f6eedcb50701e02d91cc480c
URL:		http://www.libimobiledevice.org/
BuildRequires:	libplist-devel >= 1.11
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%undefine	__cxx

%description
libusbmuxd is the client library used for communicating with Apple's
iPod Touch, iPhone, iPad and Apple TV devices. It allows multiple
services on the device to be accessed simultaneously.

%package utils
Summary:	Utilities for communicating with Apple's iOS devices
License:	GPL v2+
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description utils
Utilities for Apple's iOS devices

%package devel
Summary:	Development package for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	usbmuxd-devel < 1.0.9

%description devel
Files for development with %{name}.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	--disable-static

%{__make} %{?with_test:check}

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
%doc README AUTHORS
%attr(755,root,root) %{_libdir}/libusbmuxd.so.*.*.*
%ghost %{_libdir}/libusbmuxd.so.4

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/iproxy

%files devel
%defattr(644,root,root,755)
%{_includedir}/usbmuxd.h
%{_includedir}/usbmuxd-proto.h
%{_pkgconfigdir}/libusbmuxd.pc
%{_libdir}/libusbmuxd.so
