{
  description = "modelling env";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = nixpkgs.legacyPackages.${system};
      py = pkgs.python310;

      linopy = with py.pkgs; buildPythonPackage rec {
        pname = "linopy";
        version = "0.3.2";
        src = fetchPypi {
          inherit pname version;
          sha256 = "sha256-CPsdbOZzVJzWbu5lQxe7g/+fAb0gOKITvq0lXB+Okw0=";
        };
        doCheck = false;
        propagatedBuildInputs = [
          # linopy dependencies
          dask
        ];
      };

      pypsa = with py.pkgs; buildPythonPackage rec {
        pname = "pypsa";
        version = "0.26.2";
        src = fetchPypi {
          inherit pname version;
          sha256 = "sha256-uq/ZAF9InBNU4HBKKTLZPZJUyxBoDet70cIkCOCvw9w=";
        };
        doCheck = false;
        propagatedBuildInputs = [
          # pypsa dependencies
          black
          deprecation
          geopandas
          linopy
          networkx
          numpy
          pandas
          pyomo
          scipy
          validators
          xarray
        ];
      };

      py-deps = ps: with ps; [
        # from nixpkgs
        matplotlib
        pip

        # defined above
        linopy
        pypsa
      ];

      deps = with pkgs; [
        #bash

        (py.withPackages py-deps)
      ];

    in {
      devShells.default = pkgs.mkShell rec {
        packages = deps;

      # Environment variables
      # fixes libstdc++ issues, libz.so.1 issues
      LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib/:${pkgs.lib.makeLibraryPath packages}";
      };
    });
}
