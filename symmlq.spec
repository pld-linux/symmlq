#
# Conditional build:
%bcond_with	acml    # With ACML version of BLAS instead of NETLIB implementation
%bcond_with	atlas	# With ATLAS version of BLAS instead of NETLIB implementation
			# (mutually exclusive with acml)
#
Summary:	Iterative linear equations solver
Summary(pl):	Rozwi±zywanie równañ liniowych metod± iteracyjn±
Name:		symmlq
Version:	19991020
Release:	1%{?with_acml:ACML}%{?with_atlas:ATLAS}
License:	CPL
Group:		Libraries
Source0:	http://www.stanford.edu/group/SOL/software/symmlq/f77/symmlq.f
# Source0-md5:	8ecce1c4dfc28755229b4a34fa4b80ec
Source1:	http://www.stanford.edu/group/SOL/software/symmlq/f77/symmlq_f77.README
# Source1-md5:	83b1bfa5653f9a01758e999a1e047c79
Patch0:		%{name}-automake_support.patch
URL:		http://www.stanford.edu/group/SOL/software/symmlq.html
BuildRequires:	autoconf
BuildRequires:	automake
%{!?with_acml:%{!?with_atlas:BuildRequires:	blas-devel}}
BuildRequires:	gcc-g77
BuildRequires:	libtool >= 2:1.5
%{?with_acml:ExclusiveArch:	amd64}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Implementation of a conjugate-gradient type method for solving sparse
linear equations: solve Ax = b or (A - sI)x = b. The matrix A - sI must
be symmetric and nonsingular, but it may be definite or indefinite. The
scalar s is a shifting parameter -- it may be any number. The method is
based on Lanczos tridiagonalization. You may provide a preconditioner,
but it must be positive definite. 

%description -l pl
Implementacja gradientowej metody rozwi±zywania rzadkich uk³adów równañ
liniowych, postaci Ax = b albo (A - sI)x = b. Macierz A - sI musi byæ
symetryczna i nieosobliwa, ale nie musi byæ okre¶lona. Skalar s mo¿e byæ
dowoln± liczb±. Metoda jest oparta na trójdiagonalizacji Lanczosa. Mo¿na
jej dostarczyæ dodatnio okre¶lony preconditioner.

%package devel
Summary:	SYMMLQ development files
Summary(pl):	Pliki programistyczne SYMMLQ
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
SYMMLQ development files.

%description devel -l pl
Pliki programistyczne SYMMLQ.

%package static
Summary:	Static SYMMLQ library
Summary(pl):	Statyczna biblioteka SYMMLQ
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static SYMMLQ library.

%description static -l pl
Statyczna biblioteka SYMMLQ.

%prep
%setup -q -c -T
%patch0 -p1

cp %{SOURCE0} .
cp %{SOURCE1} README

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	CFLAGS=-O3 \
	LDFLAGS=%{?with_acml:"-lm -lg2c -lacml"}%{?with_atlas:"-lf77blas -latlas"}%{!?with_acml:%{!?with_atlas:-lblas}}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_libdir}/libsymmlq.so.*.*.*

%files devel
%defattr(644,root,root,755)
%doc symmlq.f
%attr(755,root,root) %{_libdir}/libsymmlq.so
%{_libdir}/libsymmlq.la

%files static
%defattr(644,root,root,755)
%{_libdir}/libsymmlq.a
