%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

%define library_version 1.0.4

# Running the tests requires Wine.
%define run_tests 0

Name:           mingw32-bzip2
Version:        1.0.5
Release:        8%{?dist}.4
Summary:        MinGW port of bzip2 file compression utility


License:        BSD
Group:          Development/Libraries
URL:            http://www.bzip.org/
Source0:        http://www.bzip.org/%{version}/bzip2-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

Patch0:         bzip2-1.0.4-saneso.patch
Patch5:         bzip2-1.0.4-cflags.patch
Patch6:         bzip2-1.0.4-bzip2recover.patch

Patch10:        mingw32-bzip2-1.0.5-slash.patch
Patch11:        mingw32-bzip2-1.0.5-dll.patch

BuildRequires:  mingw32-filesystem >= 49
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils

%if %{run_tests}
BuildRequires:  wine
%endif


%description
Bzip2 is a freely available, patent-free, high quality data compressor.
Bzip2 compresses files to within 10 to 15 percent of the capabilities 
of the best techniques available.  However, bzip2 has the added benefit 
of being approximately two times faster at compression and six times 
faster at decompression than those techniques.  Bzip2 is not the 
fastest compression utility, but it does strike a balance between speed 
and compression capability.

This package contains development tools and libraries for use when
cross-compiling Windows software in Fedora.


%prep
%setup -q -n bzip2-%{version}

%patch0 -p1 -b .saneso
%patch5 -p1 -b .cflags
%patch6 -p1 -b .bz2recover

%patch10 -p1 -b .slash
%patch11 -p1 -b .dll


%build
make -f Makefile-libbz2_so \
  CC="%{_mingw32_cc}" \
  AR="%{_mingw32_ar}" \
  RANLIB="%{_mingw32_ranlib}" \
  CFLAGS="%{_mingw32_cflags} -D_FILE_OFFSET_BITS=64" \
  %{?_smp_mflags} all

rm -f *.o
make CC="%{_mingw32_cc}" \
  AR="%{_mingw32_ar}" \
  RANLIB="%{_mingw32_ranlib}" \
  CFLAGS="%{_mingw32_cflags} -D_FILE_OFFSET_BITS=64" \
  %{?_smp_mflags} \
%if %{run_tests}
  all
%else
  libbz2.a bzip2 bzip2recover
%endif


%install
rm -rf $RPM_BUILD_ROOT
make PREFIX=$RPM_BUILD_ROOT%{_mingw32_prefix} install

# The binaries which are symlinks contain the full buildroot
# name in the symlink, so replace those.
pushd $RPM_BUILD_ROOT%{_mingw32_bindir}
rm bzcmp bzegrep bzfgrep bzless
ln -s bzdiff bzcmp
ln -s bzgrep bzegrep
ln -s bzgrep bzfgrep
ln -s bzmore bzless
popd

# Remove the manpages, they're duplicates of the native package,
# and located in the wrong place anyway.
rm -rf $RPM_BUILD_ROOT%{_mingw32_prefix}/man

# The Makefile doesn't install the DLL.
# Rename the library so that libtool can find it.
install bz2.dll.a $RPM_BUILD_ROOT%{_mingw32_libdir}/libbz2.dll.a
install bz2-1.dll $RPM_BUILD_ROOT%{_mingw32_bindir}/

# Remove the static library.
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libbz2.a


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc LICENSE

%{_mingw32_bindir}/bz2-1.dll
%{_mingw32_libdir}/libbz2.dll.a

%{_mingw32_bindir}/bunzip2
%{_mingw32_bindir}/bzcat
%{_mingw32_bindir}/bzcmp
%{_mingw32_bindir}/bzdiff
%{_mingw32_bindir}/bzegrep
%{_mingw32_bindir}/bzfgrep
%{_mingw32_bindir}/bzgrep
%{_mingw32_bindir}/bzip2
%{_mingw32_bindir}/bzip2recover
%{_mingw32_bindir}/bzless
%{_mingw32_bindir}/bzmore

%{_mingw32_includedir}/bzlib.h


%changelog
* Mon Dec 27 2010 Andrew Beekhof <abeekhof@redhat.com> - 1.0.5-8.4
- Rebuild everything with gcc-4.4
  Related: rhbz#658833

* Fri Dec 24 2010 Andrew Beekhof <abeekhof@redhat.com> - 1.0.5-8.3
- The use of ExclusiveArch conflicts with noarch, using an alternate COLLECTION to limit builds
  Related: rhbz#658833

* Wed Dec 22 2010 Andrew Beekhof <abeekhof@redhat.com> - 1.0.5-8.2
- Only build mingw packages on x86_64
  Related: rhbz#658833

* Wed Dec 22 2010 Andrew Beekhof <abeekhof@redhat.com> - 1.0.5-8.1
- Bump the revision to avoid tag collision
  Related: rhbz#658833

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.5-6
- Rebuild for mingw32-gcc 4.4

* Thu Dec 18 2008 Richard Jones <rjones@redhat.com> - 1.0.5-5
- Include the LICENSE file in doc section.

* Sat Nov 22 2008 Richard Jones <rjones@redhat.com> - 1.0.5-4
- Rename the implib as libbz2.dll.a so that libtool can find it.

* Wed Oct 29 2008 Richard Jones <rjones@redhat.com> - 1.0.5-3
- Fix mixed spaces/tabs in specfile.

* Fri Oct 10 2008 Richard Jones <rjones@redhat.com> - 1.0.5-2
- Allow the tests to be disabled selectively.

* Thu Sep 25 2008 Richard Jones <rjones@redhat.com> - 1.0.5-1
- Initial RPM release.
