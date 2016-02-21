Name: kibana
Version: 4.4.1
Release: 1
Summary: open source data visualization platform 
License: see /usr/share/doc/kibana/LICENSE
Distribution: Elastic
Group: Applications/Internet
Requires: td-agent >= 2.3.0
Requires: elasticsearch >= 2.2.0
%define binary_name kibana-%{version}-linux-x64
Source0: https://download.elasticsearch.org/kibana/kibana/%{binary_name}.tar.gz
Source1: https://raw.githubusercontent.com/VirtusLab/kibana-rpm-packaging/master/kibana.sysconfig
Source2: https://raw.githubusercontent.com/VirtusLab/kibana-rpm-packaging/master/kibana.service
%define _unpackaged_files_terminate_build 1
%define _basedir /opt/kibana
#Re: disable /usr/lib/rpm/find-debuginfo.sh
#https://www.redhat.com/archives/rpm-list/2004-June/msg00007.html
%define debug_package %{nil}

%description
Kibana is an open source data visualization platform that allows you to interact with your data through stunning, powerful graphics that can be combined into custom dashboards that help you share insights from your data far and wide.

%prep
%setup -q -n %{binary_name}

%build

%install
#install -m 755 -d  $RPM_BUILD_ROOT/{etc,usr/share{,/doc}}/kibana
BASEDIR=`echo %_basedir | sed -e '#^/##'`
for dirname in `find . -type d ! -name '.' -print`
do
  install -m 755 -d $RPM_BUILD_ROOT/$BASEDIR/$dirname 
done
for filename in `find . -type f ! -name '.' -print | sed -e 's#./##'`
do
  install -m 644 $filename $RPM_BUILD_ROOT/$BASEDIR/$filename
done
install -m 755 -d $RPM_BUILD_ROOT/etc/kibana/
install -m 644 config/kibana.yml $RPM_BUILD_ROOT/etc/kibana/kibana.yml
install -m 755 -d $RPM_BUILD_ROOT/etc/sysconfig
install -m 644 %SOURCE1 $RPM_BUILD_ROOT/etc/sysconfig/kibana
install -m 755 -d $RPM_BUILD_ROOT/usr/lib/systemd/system
install -m 644 %SOURCE2 $RPM_BUILD_ROOT/usr/lib/systemd/system/kibana.service
rm -rf $RPM_BUILD_ROOT/$BASEDIR/bin/*
rm -rf $RPM_BUILD_ROOT/$BASEDIR/node/bin/*
rm -rf $RPM_BUILD_ROOT/$BASEDIR/config
rm -rf $RPM_BUILD_ROOT/$BASEDIR/optimize/.babelcache.json
install -m 755 bin/kibana $RPM_BUILD_ROOT/$BASEDIR/bin/kibana
install -m 755 node/bin/node $RPM_BUILD_ROOT/$BASEDIR/node/bin/node
install -m 755 node/bin/npm $RPM_BUILD_ROOT/$BASEDIR/node/bin/npm
find $RPM_BUILD_ROOT -type d | sed -e "s#^$RPM_BUILD_ROOT/##" -e 's#^#%dir /#' > files.kibana
sed -i '1,1d' files.kibana
find $RPM_BUILD_ROOT -type f ! -name '*.py' -and ! -name "kibana.yml" -and ! -name "kibana" | sed -e "s#^$RPM_BUILD_ROOT/##" -e 's#^#/#' >> files.kibana
find $RPM_BUILD_ROOT/etc -type f | sed -e "s#^$RPM_BUILD_ROOT/##" -e 's#etc/#%config(noreplace) /etc/#' >> files.kibana
for filename in `find $RPM_BUILD_ROOT -type f -name '*.py'`
do
  echo $filename | sed -e "s#^$RPM_BUILD_ROOT/##" -e 's#^#/#' >> files.kibana
  filename=$(echo $filename | sed -e "s/\.py$/.pyc/")
  echo $filename | sed -e "s#^$RPM_BUILD_ROOT/##" -e 's#^#/#' >> files.kibana
  filename=$(echo $filename | sed -e "s/\.pyc$/.pyo/")
  echo $filename | sed -e "s#^$RPM_BUILD_ROOT/##" -e 's#^#/#' >> files.kibana
done
echo "/opt/kibana/bin/kibana" >> files.kibana
for dirname in /etc /usr/lib/systemd /usr/lib/systemd/system /etc /etc/sysconfig /opt /usr/lib /usr /opt
do
  dirname=$(echo $dirname | sed -e 's#/#\\/#g')
  sed -i -e "/$dirname\$/d" files.kibana
done

%post
if [ "$1" = 1 ]; then
  /usr/bin/chown elasticsearch:elasticsearch %_basedir/optimize/
  /usr/bin/rm -rf %_basedir/optimize/.babelcache.json
fi

%files -f files.kibana

