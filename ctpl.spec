#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static libraries
#
Summary:	C Template Parser Library
Summary(pl.UTF-8):	Biblioteka analizy szablonów w C
Name:		ctpl
Version:	0.3.4
Release:	1
License:	GPL v3+
Group:		Libraries
Source0:	http://download.tuxfamily.org/ctpl/releases/%{name}-%{version}.tar.gz
# Source0-md5:	340425537a5dada0d58f11fc6dfc4cd6
URL:		http://ctpl.tuxfamily.org/
BuildRequires:	gettext-tools >= 0.17
BuildRequires:	glib2-devel >= 1:2.24
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.9}
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
Requires:	glib2 >= 1:2.24
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CTPL (which stands for C Template (Parser) Library) is a template
engine library written in C and distributed under the terms of the GNU
GPL. It allows fast and easy parsing of templates and fine control
over template parsing environment.

%description -l pl.UTF-8
CTPL (skrót rozwijający się do C Template (Parser) Library) to
biblioteka silnika szablonów napisana w C i rozpowszechniana na
warunkach licencji GNU GPL. Umożliwia szybką i prostę analizę
szablonów z dobrą kontrolą środowiska analizującego.

%package devel
Summary:	Header files for CTPL library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki CTPL
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.24

%description devel
Header files for CTPL library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki CTPL.

%package static
Summary:	Static CTPL library
Summary(pl.UTF-8):	Statyczna biblioteka CTPL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static CTPL library.

%description static -l pl.UTF-8
Statyczna biblioteka CTPL.

%package apidocs
Summary:	API documentation for CTPL library
Summary(pl.UTF-8):	Dokumentacja API biblioteki CTPL
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for CTPL library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki CTPL.

%prep
%setup -q

%build
%configure \
	%{!?with_apidocs:--disable-gtk-doc} \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libctpl.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README THANKS TODO
%attr(755,root,root) %{_bindir}/ctpl
%attr(755,root,root) %{_libdir}/libctpl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libctpl.so.2
%{_mandir}/man1/ctpl.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libctpl.so
%{_includedir}/ctpl
%{_pkgconfigdir}/ctpl.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libctpl.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/ctpl
%endif
