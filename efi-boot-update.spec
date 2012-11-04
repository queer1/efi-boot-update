# $Revision: 1.81 $, $Date: 2012/04/20 10:52:52 $
#
Summary:	EFI bootloader updater
Name:		efi-boot-update
Version:	0.1
Release:	1
License:	GPL v2
Group:		Applications
Source0:	%{name}
Source1:	update.conf
Source2:	grub.conf
Source3:	grub-installed.conf
Source10:	README
Source11:	TODO
URL:		http://www.pld-linux.org/
BuildRequires:	help2man
Suggests:	efibootmgr
Suggests:	efi-shell-x64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir /sbin

%description
Script to update EFI bootloaders.

%prep
%setup -qcT
cp %{SOURCE0} .
cp %{SOURCE10} %{SOURCE11} .

%build
chmod a+x %{name}
help2man --no-info ./%{name} > %{name}.8

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/efi-boot/update.d
install -d $RPM_BUILD_ROOT{/lib/efi/{ia32,x64},%{_sbindir},%{_mandir}/man8}

install %{name} $RPM_BUILD_ROOT%{_sbindir}/%{name}
install %{name}.8 $RPM_BUILD_ROOT%{_mandir}/man8/%{name}.8
install %{SOURCE1} $RPM_BUILD_ROOT/etc/efi-boot
install %{SOURCE2} %{SOURCE3} $RPM_BUILD_ROOT/etc/efi-boot/update.d

%clean
rm -rf $RPM_BUILD_ROOT

# Most efi-boot-update-managed loaders will use kernel files
# even if the kernel itself is not build as EFI
%triggerin -- kernel
/sbin/efi-boot-update --auto || :
%triggerin -- kernel-longterm
/sbin/efi-boot-update --auto || :

%files
%defattr(644,root,root,755)
%doc README TODO
%attr(755,root,root) %{_sbindir}/%{name}
%dir /etc/efi-boot
%config(noreplace) %verify(not md5 mtime size) /etc/efi-boot/update.conf
%config(noreplace) %verify(not md5 mtime size) /etc/efi-boot/update.d/*.conf
%dir /etc/efi-boot/update.d
%dir /lib/efi
%dir /lib/efi/ia32
%dir /lib/efi/x64
%{_mandir}/man8/%{name}.8*
