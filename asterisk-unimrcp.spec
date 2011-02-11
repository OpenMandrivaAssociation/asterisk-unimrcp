%define svnrelease 1798

Name: asterisk-unimrcp
Version: 0.%svnrelease
Release: %mkrel 0

Summary: Media Resource Control Protocol Stack
License: Apache
Group: System/Libraries
Url: http://unimrcp.org
BuildRoot: %{_tmppath}/%{name}-%{version}

Source: %{name}.tar.gz

BuildRequires: asterisk-devel
BuildRequires: libunimrcp-devel

Requires: asterisk
Requires: libunimrcp

%description
Media Resource Control Protocol (MRCP) allows to control media processing
resources over the network using distributed client/server architecture.
Media processing resources include:
- Speech Synthesizer (TTS)
- Speech Recognizer (ASR)
- Speaker Verifier (SV)
- Speech Recorder (SR)

%package -n asterisk-unimrcp-devel
Summary: Media Resource Control Protocol Stack development
Group: Development/C
Requires: asterisk-unimrcp = %version-%release

%description -n asterisk-unimrcp-devel
Development files for asterisk-unimrcp

%prep
%setup -q -n %{name}

%build
[ ! -x ./bootstrap ] || ./bootstrap
perl -pi -w -e 's/lib\/pkgconfig/pkgconfig/g' configure
perl -pi -w -e 's/UNIMRCP_DIR_LOCATION \"\$unimrcp_dir\"/UNIMRCP_DIR_LOCATION \"\/etc\/unimrcp\"/g' configure

%configure2_5x \
    LDFLAGS=-rpath=%{_datadir}/unimrcp-deps/lib \
    --sysconfdir=%{_sysconfdir}/asterisk \
    --with-unimrcp=%{_libdir} \
    --prefix=%{_libdir}/asterisk/modules

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
%makeinstall_std DESTDIR=%{buildroot} install

install -d -m1775 %{buildroot}%{_sysconfdir}/asterisk
install -m0664 conf/*.conf %{buildroot}%{_sysconfdir}/asterisk/

%clean
rm -fr %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/asterisk/modules/*.so
%config(noreplace) %{_sysconfdir}/asterisk/*.conf

%files -n asterisk-unimrcp-devel
%defattr(-,root,root)
%{_libdir}/asterisk/modules/*.a
%{_libdir}/asterisk/modules/*.la
