# Enable the automatic Python dependency generator
%{?python_enable_dependency_generator}

# Tests do not work without vagrant + virtualbox in the environment
%bcond_with tests

%global pypi_name vagrantpy

Name:           python-%{pypi_name}
Version:        0.6.0
Release:        0%{?dist}
Summary:        Python bindings for interacting with Vagrant virtual machines

%if %{_vendor} == "debbuild"
Packager:       David McCheyne <davidmccheyne@gmail.com>
Group:          python
%endif

License:        MIT
URL:            https://github.com/vagrantpy/vagrantpy
Source0:        https://files.pythonhosted.org/packages/source/v/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

%if %{_vendor} == "debbuild"
BuildRequires:  python3-dev
BuildRequires:  python3-setuptools
BuildRequires:  python3-deb-macros
%else
BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)
%endif

%if %{with tests}
BuildRequires:  python3dist(nose)
BuildRequires:  python3dist(rednose)
BuildRequires:  vagrant
BuildRequires:  virtualbox
%endif

%description
VagrantPy is a python module that provides a _thin_ wrapper
around the vagrant command line executable, allowing programmatic control of
Vagrant virtual machines (boxes).

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}
%if %{_vendor} == "debbuild"
Requires(preun): python3-minimal
Requires(post): python3-minimal
%endif

%description -n python3-%{pypi_name}
VagrantPy is a python module that provides a _thin_ wrapper
around the vagrant command line executable, allowing programmatic control of
Vagrant virtual machines (boxes).


%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%if %{with tests}
%check
nosetests --immediate --stop -vv --rednose
%endif

%files -n python3-%{pypi_name}
%license LICENSE.txt
%doc README.md
%{python3_sitelib}/vagrant
%{python3_sitelib}/vagrantpy-%{version}-*

%if %{_vendor} == "debbuild"
%preun -n python3-%{pypi_name}
%{py3_bytecompile_preun python3-%{pypi_name}}

%post -n python3-%{pypi_name}
%{py3_bytecompile_post python3-%{pypi_name}}
%endif

%changelog
* Wed Jan 15 2020 Neal Gompa <ngompa13@gmail.com>
- Initial packaging
