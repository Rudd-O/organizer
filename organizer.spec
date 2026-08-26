# See https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_example_spec_file

%define debug_package %{nil}

%define _name organizer

%define mybuildnumber %{?build_number}%{?!build_number:1}

Name:           %{_name}
Version:        0.0.14
Release:        %{mybuildnumber}%{?dist}
Summary:        A tool to assist in organizing media files

License:        GPLv3+
URL:            https://github.com/Rudd-O/%{_name}
Source:         %{_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel python3-setuptools
BuildRequires:  desktop-file-utils
BuildRequires:  coreutils

Requires:       python3-iniparse python3-jinja2 kdialog python3-decorator

%global _description %{expand:
The organizer will help you sort your media files in folders easily
and conveniently.}

%description %_description

%prep
%autosetup -p1

%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install --dir=%{buildroot}%{_datadir}/applications src/%{_name}/applications/%{_name}.desktop

%pyproject_save_files %{_name}
echo %{_bindir}/%{_name} >> %{pyproject_files}
echo %{_datadir}/applications/%{_name}.desktop >> %{pyproject_files}


%check
# no percent tox


%files -f %{pyproject_files}

%doc README.md TODO.md


%changelog
* Wed Feb 21 2024 Manuel Amador <rudd-o@rudd-o.com> 0.0.26-1
- First RPM packaging release
