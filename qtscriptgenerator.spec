Name:          qtscriptgenerator
Version:       0.1.0
Release:       %mkrel 1
Summary:       A tool to generate Qt bindings for Qt Script    
Group:         System/Libraries
License:       GPLv2   
URL:           http://code.google.com/p/qtscriptgenerator/ 
Source0:       http://qtscriptgenerator.googlecode.com/files/qtscriptgenerator-src-%{version}.tar.gz   
Patch0:        qtscriptgenerator-src-0.1.0-fix-strings.patch
Patch1:        include_everything.patch
Patch2:        qtscriptgenerator-src-0.1.0-fix-build.patch
BuildRoot:     %_tmppath/%name-%version-%release-root
BuildRequires: libxslt-proc
BuildRequires: phonon-devel >= 4.3.1
BuildRequires: qt4-devel >= 3:4.5.0

# not strictly required, but the expectation would be for the 
# bindings to be present
Requires:      qtscriptbindings = %{version}-%{release}

%description
Qt Script Generator is a tool to generate Qt bindings for Qt Script.

%files
%defattr(-,root,root,-)
%{qt4bin}/generator

#--------------------------------------------------------------------

%package -n qtscriptbindings 
Summary:    Qt bindings for Qt Script
Group:      System/Libraries
Provides:   qtscript-qt = %{version}-%{release}
Requires:   qt4 >= 3:4.4.5

%description -n qtscriptbindings
Bindings providing access to substantial portions of the Qt API
from within Qt Script.

%files -n qtscriptbindings
%defattr(-,root,root,-)
%doc README LICENSE.GPL
%doc README.qsexec
%doc doc/
%doc examples/
%{_bindir}/qsexec
%{qt4plugins}/script/libqtscript*

#--------------------------------------------------------------------

%prep
%setup -q -n %{name}-src-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p0

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
make %{?_smp_mflags}
popd
 
pushd tools/qsexec/src
%{qmake_qt4} qsexec.pro
make  %{?_smp_mflags}
popd


%install
rm -rf %{buildroot} 

mkdir -p %{buildroot}%{qt4plugins}/script/
# install doesn't do symlinks
cp -a plugins/script/libqtscript* \
  %{buildroot}%{qt4plugins}/script/

cp -a tools/qsexec/README.TXT README.qsexec
install -D -p -m755 tools/qsexec/qsexec %{buildroot}%{_bindir}/qsexec

install -D -p -m755 generator/generator %{buildroot}%{qt4bin}/generator

%clean
rm -rf %{buildroot} 
