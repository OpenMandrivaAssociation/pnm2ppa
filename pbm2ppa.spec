Summary:	PNM2PPA GhostScript Print Filter
Name:		pnm2ppa
Version:	1.12
Release:	%mkrel 11
Group:		System/Printing
License:	GPL
URL:		http://pnm2ppa.sourceforge.net/
Source0:	http://downloads.sourceforge.net/pnm2ppa/%{name}-%{version}.tar.gz
#Source1:	http://www.httptech.com/ppa/files/ppa-0.8.6.tar.bz2
Source1:	http://fresh.t-systems-sfr.com/linux/src/ppa-0.8.6.tar.gz
Patch0:		pbm2ppa-20000205.diff
Patch1:		pnm2ppa-mdv_conf.diff
Patch2:		pbm2ppa-mdv_conf.diff
Patch3:		pnm2ppa-1.12-LDFLAGS.diff
Conflicts:	printer-utils = 2007
Conflicts:	printer-filters = 2007
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
PPA (Printing Performance Architecture) is a closed, proprietary protocol
developed by Hewlett Packard for a short-lived series of DeskJet printers. In
essence, the PPA protocol moves the low-level processing of the data to the
host computer rather than the printer. This allows for a low-cost (to produce)
printer with a small amount of memory and computing power. However, in practice
the printer was often as expensive as more capable printers and HP has since
discontinued the use of PPA in favour of returning to PCL3e in their latest
USB-based printers.

%prep

%setup -q -a1

# fix attribs
find -type f | xargs chmod 644

%patch0 -p1
%patch1 -p0
%patch2 -p0
%patch3 -p1

# remove "version ERROR" line from pnm2ppa.conf
perl -n -i -e 'if ( !m/^\s*version\s*0\s*(|\#.*)$/ ) { print "$_";}' pnm2ppa-*/pnm2ppa.conf

# Generate README file
cat > README.calibration << EOF

Colour calibration for PPA printers
-----------------------------------

If you have an HP DeskJet PPA printer (very cheap models: 710C, 712C,
720C, 722C, 820C, 1000C, or a newer printer which works with one of
these model entries) you can optionally do a colour correction. Do the
following:

Some of the printing modes offer optional colour correction. See the
option "Printing Mode" which is offered to you in the option window of
"printerdrake" and if you use CUPS also in "qtcups" or "kprinter"
("Properties" button, "Advanced" tab), "xpp" ("Options" button,
"Extra" tab), "kups" (right click on printer, "Configure printer" in
menu), or the WWW interface ("Configure printer" button) and if you
use PDQ in "xpdq" ("Driver options"). Choose a setting with "optional
colour correction" and save your settings. Read the file

    %{_docdir}/%{name}*/COLOR.txt

and follow the instructions there, but use the name

   /etc/pnm2ppa.gamma_normal

for the colour correction file for the "normal quality" modes and

   /etc/pnm2ppa.gamma_best

for the colour correction file for the "best quality" modes. So you
can do the colour correction independently in both normal and best
quality modes. The files are automatically taken into account by the
appropriate modes as soon as they are created.
EOF

%build

%make RPM_OPT_FLAGS="%{optflags}" LDFLAGS="%{ldflags}"

%make -C pbm2ppa-* RPM_OPT_FLAGS="%{optflags}" LDFLAGS="%{ldflags}"

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_mandir}/man1

%makeinstall_std

install -m 0755 utils/Linux/detect_ppa %{buildroot}%{_bindir}/
install -m 0755 utils/Linux/test_ppa %{buildroot}%{_bindir}/

install -m 0755 pbm2ppa-*/pbm2ppa %{buildroot}%{_bindir}/
install -m 0755 pbm2ppa-*/pbmtpg %{buildroot}%{_bindir}/
install -m 0644 pbm2ppa-*/pbm2ppa.conf %{buildroot}%{_sysconfdir}/
install -m 0644 pbm2ppa-*/pbm2ppa.1 %{buildroot}%{_mandir}/man1/

for i in CALIBRATION CREDITS INSTALL INSTALL-MORE README; do
    cp pbm2ppa-*/$i $i.pbm2ppa
done

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc Changelog README.calibration README.security test.ps testpage-a4.ps testpage.ps
%doc docs/en/CALIBRATION.txt docs/en/COLOR.txt docs/en/CREDITS docs/en/INSTALL docs/en/INSTALL.MANDRAKE.txt
%doc docs/en/LICENSE docs/en/PPA_networking.txt docs/en/README docs/en/RELEASE-NOTES docs/en/TODO *.pbm2ppa
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pnm2ppa.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pbm2ppa.conf
%attr(0755,root,root) %{_bindir}/calibrate_ppa
%attr(0755,root,root) %{_bindir}/detect_ppa
%attr(0755,root,root) %{_bindir}/pbm2ppa
%attr(0755,root,root) %{_bindir}/pbmtpg
%attr(0755,root,root) %{_bindir}/pnm2ppa
%attr(0755,root,root) %{_bindir}/test_ppa
%attr(0644,root,root) %{_mandir}/man1/pnm2ppa.1*
%attr(0644,root,root) %{_mandir}/man1/pbm2ppa.1*


%changelog
* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 1.12-10mdv2011.0
+ Revision: 667794
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 1.12-9mdv2011.0
+ Revision: 607186
- rebuild

* Sun Mar 14 2010 Oden Eriksson <oeriksson@mandriva.com> 1.12-8mdv2010.1
+ Revision: 519054
- rebuild

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.12-7mdv2010.0
+ Revision: 426734
- rebuild

* Thu Dec 25 2008 Oden Eriksson <oeriksson@mandriva.com> 1.12-6mdv2009.1
+ Revision: 319070
- rediffed one fuzzy patch
- use %%ldflags

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 1.12-5mdv2009.0
+ Revision: 225019
- rebuild

* Tue Mar 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1.12-4mdv2008.1
+ Revision: 179239
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - fix no-buildroot-tag
    - kill re-definition of %%buildroot on Pixel's request

* Thu Aug 30 2007 Oden Eriksson <oeriksson@mandriva.com> 1.12-3mdv2008.0
+ Revision: 75354
- fix deps (pixel)

* Thu Aug 16 2007 Oden Eriksson <oeriksson@mandriva.com> 1.12-2mdv2008.0
+ Revision: 64173
- use the new System/Printing RPM GROUP

* Mon Aug 13 2007 Oden Eriksson <oeriksson@mandriva.com> 1.12-1mdv2008.0
+ Revision: 62603
- Import pnm2ppa



* Mon Aug 13 2007 Oden Eriksson <oeriksson@mandriva.com> 1.12-1mdv2008.0
- initial Mandriva package
