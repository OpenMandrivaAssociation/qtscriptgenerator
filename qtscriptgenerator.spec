%define debug_package %{nil}

Summary:	A tool to generate Qt bindings for Qt Script    
Name:		qtscriptgenerator
Version:	0.2.0
Release:	9
Group:		System/Libraries
License:	GPLv2   
Url:		http://code.google.com/p/qtscriptgenerator/ 
Source0:	http://qtscriptgenerator.googlecode.com/files/qtscriptgenerator-src-%{version}.tar.gz
Source100:	%{name}.rpmlintrc
Patch0:		qtscriptgenerator-src-0.1.0-fix-strings.patch
Patch1:		include_everything.patch
Patch2:		qtscriptgenerator-src-0.1.0-fix-build.patch
Patch3:		memory_alignment_fix.diff
## upstreamable patches
Patch4:		qtscriptgenerator-src-0.1.0-qmake_target.path.patch
# fix arm ftbfs, kudos to mamba
Patch5:		qtscriptgenerator-0.2.0-arm-ftbfs-float.patch
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	qt4-devel
BuildRequires:	pkgconfig(phonon)
BuildRequires:	pkgconfig(QtWebKit)
# not strictly required, but the expectation would be for the 
# bindings to be present
Requires:	qtscriptbindings = %{version}-%{release}

%description
Qt Script Generator is a tool to generate Qt bindings for Qt Script.

%files
%{qt4bin}/generator

#--------------------------------------------------------------------

%package -n qtscriptbindings 
Summary:	Qt bindings for Qt Script
Group:		System/Libraries
Provides:	qtscript-qt = %{version}-%{release}
Requires:	qt4-common

%description -n qtscriptbindings
Bindings providing access to substantial portions of the Qt API
from within Qt Script.

%files -n qtscriptbindings
%doc README
%doc README.qsexec
%doc doc/
%doc examples/
%{_bindir}/qsexec
%{qt4plugins}/script/libqtscript*

#--------------------------------------------------------------------

%prep
%setup -qn %{name}-src-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
# workaround buildsys bogosity, see also:
# http://code.google.com/p/qtscriptgenerator/issues/detail?id=38
export INCLUDE=%{qt4include}

pushd generator 
%{qmake_qt4} generator.pro
make
./generator
popd

pushd qtbindings
%{qmake_qt4} qtbindings.pro
%make
popd
 
pushd tools/qsexec/src
%{qmake_qt4} qsexec.pro
%make
popd


%install
mkdir -p %{buildroot}%{qt4plugins}/script/
# install doesn't do symlinks
cp -a plugins/script/libqtscript* \
  %{buildroot}%{qt4plugins}/script/

cp -a tools/qsexec/README.TXT README.qsexec
install -D -p -m755 tools/qsexec/qsexec %{buildroot}%{_bindir}/qsexec
install -D -p -m755 generator/generator %{buildroot}%{qt4bin}/generator

