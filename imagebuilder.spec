
#debuginfo not supported with Go
%global debug_package %{nil}

# modifying the Go binaries breaks the DWARF debugging
%global __os_install_post %{_rpmconfigdir}/brp-compress

# %commit and %os_git_vars are intended to be set by tito custom builders provided
# in the .tito/lib directory. The values in this spec file will not be kept up to date.
%{!?commit: %global commit HEAD }
%global shortcommit %(c=%{commit}; echo ${c:0:7})

#
# Customize from here.
#

%global golang_version 1.8.1
%{!?version: %global version 0.0.1}
%{!?release: %global release 1}
%global package_name imagebuilder
%global product_name Container Image Builder
%global import_path github.com/openshift/imagebuilder

Name:           %{package_name}
Version:        %{version}
Release:        %{release}%{?dist}
Summary:        Builds Dockerfile using the Docker client
License:        ASL 2.0
URL:            https://%{import_path}

Source0:        https://%{import_path}/archive/%{commit}/%{name}-%{version}.tar.gz
BuildRequires:  golang >= %{golang_version}

# If go_arches not defined fall through to implicit golang archs
%if 0%{?go_arches:1}
ExclusiveArch:  %{go_arches}
%else
ExclusiveArch:  x86_64 aarch64 ppc64le s390x
%endif

### AUTO-BUNDLED-GEN-ENTRY-POINT

%description
Builds Dockerfile using the Docker client.

%prep
%setup -q

%build
go build cmd/imagebuilder/imagebuilder.go

%install

PLATFORM="$(go env GOHOSTOS)/$(go env GOHOSTARCH)"
install -d %{buildroot}%{_bindir}

# Install linux components
for bin in imagebuilder
do
  echo "+++ INSTALLING ${bin}"
  install -p -m 755 _output/local/bin/${PLATFORM}/${bin} %{buildroot}%{_bindir}/${bin}
done

%files
%doc README.md
%license LICENSE
%{_bindir}/imagebuilder

%pre

%changelog
* Mon Nov 06 2017 Anonymous <anon@nowhere.com> 0.0.1
- Initial example of spec.
