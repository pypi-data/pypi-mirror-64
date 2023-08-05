# Copyright Toyota Research Institute 2019

import abc
import warnings
import json
import pickle
import os
import numpy as np
import itertools
from camd import tqdm
from camd.log import camd_traced
from qmpy.analysis.thermodynamics.phase import Phase, PhaseData
from qmpy.analysis.thermodynamics.space import PhaseSpace
import multiprocessing
from pymatgen import Composition
from pymatgen.entries.computed_entries import ComputedEntry
from pymatgen.analysis.phase_diagram import PhaseDiagram, PDPlotter, tet_coord,\
    triangular_coord
from pymatgen.analysis.structure_matcher import StructureMatcher
from pymatgen import Structure, Element
from camd.utils.data import cache_matrio_data
from camd import CAMD_CACHE
from monty.os import cd
from monty.serialization import loadfn

ELEMENTS = ['Ru', 'Re', 'Rb', 'Rh', 'Be', 'Ba', 'Bi', 'Br', 'H', 'P',
            'Os', 'Ge', 'Gd', 'Ga', 'Pr', 'Pt', 'Pu', 'C', 'Pb', 'Pa',
            'Pd', 'Xe', 'Pm', 'Ho', 'Hf', 'Hg', 'He', 'Mg', 'K', 'Mn',
            'O', 'S', 'W', 'Zn', 'Eu', 'Zr', 'Er', 'Ni', 'Na', 'Nb',
            'Nd', 'Ne', 'Np', 'Fe', 'B', 'F', 'Sr', 'N', 'Kr', 'Si',
            'Sn', 'Sm', 'V', 'Sc', 'Sb', 'Se', 'Co', 'Cl', 'Ca', 'Ce',
            'Cd', 'Tm', 'Cs', 'Cr', 'Cu', 'La', 'Li', 'Tl', 'Lu', 'Th',
            'Ti', 'Te', 'Tb', 'Tc', 'Ta', 'Yb', 'Dy', 'I', 'U', 'Y', 'Ac',
            'Ag', 'Ir', 'Al', 'As', 'Ar', 'Au', 'In', 'Mo']


class AnalyzerBase(abc.ABC):
    @abc.abstractmethod
    def analyze(self):
        """
        Performs the analysis procedure associated with the analyzer

        Returns:
            Some arbitrary result

        """

    @abc.abstractmethod
    def present(self):
        """
        Formats the analysis into a some presentation-oriented
        document

        Returns:
            json document for presentation, e. g. on a web frontend

        """


@camd_traced
class AnalyzeStructures(AnalyzerBase):
    """
    This class tests if a list of structures are unique. Typically
    used for comparing hypothetical structures (post-DFT relaxation)
    and those from ICSD.
    """
    def __init__(self, structures=None, hull_distance=None):
        self.structures = structures if structures else []
        self.structure_ids = None
        self.unique_structures = None
        self.groups = None
        self.energies = None
        self.against_icsd = False
        self.structure_is_unique = None
        self.hull_distance = hull_distance
        super(AnalyzeStructures, self).__init__()

    def analyze(self, structures=None, structure_ids=None,
                against_icsd=False, energies=None):
        """
        One encounter of a given structure will be labeled as True, its
        remaining matching structures as False.

        Args:
            structures (list): a list of structures to be compared.
            structure_ids (list): uids of structures, optional.
            against_icsd (bool): whether a comparison to icsd is also made.
            energies (list): list of energies (per atom) corresponding
                to structures. If given, the lowest energy instance of a
                given structure will be return as the unique one. Otherwise,
                there is no such guarantee. (optional)
        Returns:
            ([bool]) list of bools corresponding to the given list of
                structures corresponding to uniqueness
        """
        self.structures = structures
        self.structure_ids = structure_ids
        self.against_icsd = against_icsd
        self.energies = energies

        smatch = StructureMatcher()
        self.groups = smatch.group_structures(structures)
        self.structure_is_unique = []

        if self.energies:
            for i in range(len(self.groups)):
                self.groups[i] = [x for _, x in sorted(
                    zip([self.energies[self.structures.index(s)]
                         for s in self.groups[i]], self.groups[i]))]

        self._unique_structures = [i[0] for i in self.groups]
        for s in structures:
            if s in self._unique_structures:
                self.structure_is_unique.append(True)
            else:
                self.structure_is_unique.append(False)
        self._not_duplicate = self.structure_is_unique

        if self.against_icsd:
            structure_file = "oqmd1.2_exp_based_entries_structures.json"
            cache_matrio_data(structure_file)
            with open(os.path.join(CAMD_CACHE, structure_file), 'r') as f:
                icsd_structures = json.load(f)
            chemsys = set()
            for s in self._unique_structures:
                chemsys = chemsys.union( set(s.composition.as_dict().keys()))

            self.icsd_structs_inchemsys = []
            for k, v in icsd_structures.items():
                try:
                    s = Structure.from_dict(v)
                    elems = set(s.composition.as_dict().keys())
                    if elems == chemsys:
                        self.icsd_structs_inchemsys.append(s)
                except:
                    warnings.warn("Unable to process structure {}".format(k))

            self.matching_icsd_strs = []
            for i in range(len(structures)):
                if self.structure_is_unique[i]:
                    match = None
                    for s2 in self.icsd_structs_inchemsys:
                        if smatch.fit(self.structures[i], s2):
                            match = s2
                            break
                    self.matching_icsd_strs.append(match) # store the matching ICSD structures.
                else:
                    self.matching_icsd_strs.append(None)

            # Flip matching bools, and create a filter
            self._icsd_filter = [not i for i in self.matching_icsd_strs]
            self.structure_is_unique = (np.array(self.structure_is_unique)
                                        * np.array(self._icsd_filter)).tolist()
            self.unique_structures = list(itertools.compress(
                self.structures, self.structure_is_unique))
        else:
            self.unique_structures = self._unique_structures

        # We store the final list of unique structures as unique_structures.
        # We return a corresponding list of bool to the initial structure
        # list provided.
        return self.structure_is_unique

    def analyze_vaspqmpy_jobs(self, jobs, against_icsd=False,
                              use_energies=False):
        """
        Useful for analysis integrated as part of a campaign itself

        Args:
            jobs:
            against_icsd:

        Returns:
        """
        self.structure_ids = []
        self.structures = []
        self.energies = []
        for j, r in jobs.items():
            if r['status'] == 'SUCCEEDED':
                self.structures.append(r['result']['output']['crystal'])
                self.structure_ids.append(j)
                self.energies.append(r['result']['output']['final_energy_per_atom'])
        if use_energies:
            return self.analyze(self.structures, self.structure_ids,
                                against_icsd, self.energies)
        else:
            return self.analyze(self.structures, self.structure_ids, against_icsd)

    def present(self):
        pass


class FinalizeQqmdCampaign:
    def __init__(self, hull_distance=None):
        self.hull_distance = hull_distance if hull_distance else 0.2
        self.path = None

    def finalize(self, path=None):
        """
        post-processing for dft-campaigns
        """
        self.path = path if path else '.'
        update_run_w_structure(self.path, hull_distance=self.hull_distance)


class AnalyzeStability(AnalyzerBase):
    def __init__(self, df=None, new_result_ids=None, hull_distance=None,
                 multiprocessing=True, entire_space=False):
        self.df = df
        self.new_result_ids = new_result_ids
        self.hull_distance = hull_distance if hull_distance else 0.05
        self.multiprocessing = multiprocessing
        self.entire_space = entire_space
        self.space = None
        self.stabilities = None
        super(AnalyzeStability, self).__init__()

    def filter_dataframe_by_composition(self, elements, df=None):
        """
        Filters dataframe by composition
        """
        df = df if df is not None else self.df
        elements = set(elements)
        ind_to_include = []
        for ind in self.df.index:
            if set(Composition(df.loc[ind]['Composition']).as_dict().keys()).issubset(elements):
                ind_to_include.append(ind)
        return df.loc[ind_to_include]

    def get_phase_space(self, df=None):
        """
        Gets PhaseSpace object associated with dataframe
        """
        _df = df if df is not None else self.df
        phases = []
        for data in _df.iterrows():
            phases.append(Phase(data[1]['Composition'], energy=data[1]['delta_e'],
                                per_atom=True, description=data[0]))
        for el in ELEMENTS:
            phases.append(Phase(el, 0.0, per_atom=True))

        pd = PhaseData()
        pd.add_phases(phases)
        space = PhaseSpaceAL(bounds=ELEMENTS, data=pd)
        return space

    def analyze(self, df=None, new_result_ids=None, all_result_ids=None,
                return_within_hull=True):
        """
        Args:
            df (DataFrame): data frame with structure-data for formation
                energy, composition, etc.
            new_result_ids (list): list of ids from the dataframe index
                corresponding to new results
            all_result_ids (list): list of ids from the dataframe index
                corresponding to all desired analyzed results
            return_within_hull (bool): whether to return boolean array
                corresponding to whether stabilities are within hull
                or raw results

        Returns:

        """
        include_columns = ['Composition', 'delta_e']
        self.df = df[include_columns].drop_duplicates(keep='last').dropna()
        # Note some of id's in all_result_ids may not have corresponding
        # experiment, if those exps. failed.
        self.all_result_ids = all_result_ids
        self.new_result_ids = new_result_ids

        if not self.entire_space:
            # Constrains the phase space to that of the target compounds.
            # More efficient when searching in a specified chemistry,
            # less efficient if larger spaces are without specified chemistry.
            comps = self.df.loc[all_result_ids]['Composition'].dropna()
            system_elements = []
            for comp in comps:
                system_elements += list(Composition(comp).as_dict().keys())
            # TODO: Fix this line to be compatible with
            # later versions of pandas (i.e. b/c all_result_ids may contain
            # things not in df currently (b/c of failed experiments).
            # We should test comps = self.df.loc[self.df.index.intersection(all_result_ids)]
            _df = self.filter_dataframe_by_composition(system_elements)
        else:
            _df = self.df

        space = self.get_phase_space(_df)

        if all_result_ids is not None:
            all_new_phases = [p for p in space.phases if p.description in all_result_ids]
        else:
            all_new_phases = None

        if self.multiprocessing:
            space.compute_stabilities_multi(phases_to_evaluate=all_new_phases)
        else:
            space.compute_stabilities_mod(phases_to_evaluate=all_new_phases)

        self.space = space

        # Key stabilities by ID
        stabilities_by_id = {phase.description: phase.stability
                             for phase in all_new_phases}
        self.stabilities = stabilities_by_id

        # Get stabilities of new and all ids
        stabilities_of_new = np.array([stabilities_by_id.get(uid, np.nan)
                                       for uid in self.new_result_ids], dtype=np.float)
        stabilities_of_all = np.array([stabilities_by_id.get(uid, np.nan)
                                       for uid in self.all_result_ids], dtype=np.float)

        # Cast to boolean if specified
        if return_within_hull:
            stabilities_of_new = stabilities_of_new <= self.hull_distance
            stabilities_of_all = stabilities_of_all <= self.hull_distance

        return stabilities_of_new, stabilities_of_all

    def present(self, df=None, new_result_ids=None, all_result_ids=None,
                filename=None, save_hull_distance=False, finalize=False):
        """
        Generate plots of convex hulls for each of the runs

        Args:
            df (DataFrame): dataframe with formation energies, compositions, ids
            new_result_ids ([]): list of new result ids (i. e. indexes
                in the updated dataframe)
            all_result_ids ([]): list of all result ids associated
                with the current run
            filename (str): filename to output, if None, no file output
                is produced

        Returns:
            (pyplot): plotter instance
        """
        df = df if df is not None else self.df
        new_result_ids = new_result_ids if new_result_ids is not None \
            else self.new_result_ids
        all_result_ids = all_result_ids if all_result_ids is not None \
            else self.all_result_ids

        # TODO: consolidate duplicated code here
        # Generate all entries
        comps = df.loc[all_result_ids]['Composition'].dropna()
        system_elements = []
        for comp in comps:
            system_elements += list(Composition(comp).as_dict().keys())
        elems = set(system_elements)
        if len(elems) > 4:
            warnings.warn("Number of elements too high for phase diagram plotting")
            return None
        ind_to_include = []
        for ind in df.index:
            if set(Composition(df.loc[ind]['Composition']).as_dict().keys()).issubset(elems):
                ind_to_include.append(ind)
        _df = df.loc[ind_to_include]

        # Create computed entry column
        _df['entry'] = [
            ComputedEntry(
                Composition(row['Composition']),
                row['delta_e'] * Composition(row['Composition']).num_atoms,  # un-normalize the energy
                entry_id=index
            )
            for index, row in _df.iterrows()]
        # Partition ids into sets of prior to CAMD run, from CAMD but prior to
        # current iteration, and new ids
        ids_prior_to_camd = list(set(_df.index) - set(all_result_ids))
        ids_prior_to_run = list(set(all_result_ids) - set(new_result_ids))

        # Create phase diagram based on everything prior to current run
        entries = list(_df.loc[ids_prior_to_run + ids_prior_to_camd]['entry'])
        # Filter for nans by checking if it's a computed entry
        entries = [entry for entry in entries if isinstance(entry, ComputedEntry)]
        pg_elements = [Element(el) for el in sorted(elems)]
        pd = PhaseDiagram(entries, elements=pg_elements)
        plotkwargs = {
            "markerfacecolor": "white",
            "markersize": 7,
            "linewidth": 2,
        }
        if finalize:
            plotkwargs.update({'linestyle': '--'})
        else:
            plotkwargs.update({'linestyle': '-'})
        plotter = PDPlotter(pd, **plotkwargs)

        getplotkwargs = {"label_stable": False} if finalize else {}
        plot = plotter.get_plot(**getplotkwargs)
        # Get valid results
        valid_results = [new_result_id for new_result_id in new_result_ids
                         if new_result_id in _df.index]

        if finalize:
            # If finalize, we'll reset pd to all entries at this point
            # to measure stabilities wrt. the ultimate hull.
            pd = PhaseDiagram(_df['entry'].values, elements=pg_elements)
            plotter = PDPlotter(pd, **{"markersize": 0, "linestyle": "-", "linewidth": 2})
            plot = plotter.get_plot(plt=plot)

        for entry in _df['entry'][valid_results]:
            decomp, e_hull = pd.get_decomp_and_e_above_hull(
                    entry, allow_negative=True)
            if e_hull < self.hull_distance:
                color = 'g'
                marker = 'o'
                markeredgewidth = 1
            else:
                color = 'r'
                marker = 'x'
                markeredgewidth = 1

            # Get coords
            coords = [entry.composition.get_atomic_fraction(el)
                      for el in pd.elements][1:]
            if pd.dim == 2:
                coords = coords + [pd.get_form_energy_per_atom(entry)]
            if pd.dim == 3:
                coords = triangular_coord(coords)
            elif pd.dim == 4:
                coords = tet_coord(coords)
            plot.plot(*coords, marker=marker, markeredgecolor=color,
                      markerfacecolor="None", markersize=11,
                      markeredgewidth=markeredgewidth)

        if filename is not None:
            plot.savefig(filename, dpi=70)
        plot.close()

        if filename is not None and save_hull_distance:
            if self.stabilities is None:
                print("ERROR: No stability information in analyzer.")
                return None
            with open(filename.split(".")[0]+'.json', 'w') as f:
                json.dump(self.stabilities, f)


class PhaseSpaceAL(PhaseSpace):
    """
    Modified qmpy.PhaseSpace for GCLP based stabiltiy computations
    TODO: basic multithread or Gurobi for gclp
    """

    def compute_stabilities_mod(self, phases_to_evaluate=None):
        """
        Calculate the stability for every Phase.

        Args:
            phases_to_evaluate ([phase]): Included phases, if None,
                uses every Phase in PhaseSpace.phases
        """

        if phases_to_evaluate is None:
            phases_to_evaluate = self.phases

        for p in tqdm(list(self.phase_dict.values())):
            if p.stability is None:  # for low e phases, we only need to eval stability if it doesn't exist
                try:
                    p.stability = p.energy - self.gclp(p.unit_comp)[0]
                except:
                    print(p)
                    p.stability = np.nan

        # will only do requested phases for things not in phase_dict
        for p in tqdm(phases_to_evaluate):
            if p not in list(self.phase_dict.values()):
                if p.name in self.phase_dict:
                    p.stability = p.energy - self.phase_dict[p.name].energy + self.phase_dict[p.name].stability
                else:
                    try:
                        p.stability = p.energy - self.gclp(p.unit_comp)[0]
                    except:
                        print(p)
                        p.stability = np.nan

    def compute_stabilities_multi(self, phases_to_evaluate=None,
                                  ncpus=multiprocessing.cpu_count()):
        """
        Calculate the stability for every Phase using multiprocessing

        Args:
            phases_to_evaluate ([phase]): Included phases, if None,
                uses every Phase in PhaseSpace.phases
            ncpus (int): number of cpus to use in multiprocessing
        """

        if phases_to_evaluate is None:
            phases_to_evaluate = self.phases

        # Creating a map from entry uid to index of entry in the
        # current list of phases in space.
        self.uid_to_phase_ind = dict([(self.phases[i].description, i)
                                      for i in range(len(self.phases))])

        phase_dict_list = list(self.phase_dict.values())
        _result_list1 = parmap(self._multiproc_help1,
                               phase_dict_list, nprocs=ncpus)
        for i in range(len(phase_dict_list)):
            self.phase_dict[phase_dict_list[i].name].stability = _result_list1[i]

        _result_list2 = parmap(self._multiproc_help2,
                               phases_to_evaluate, nprocs=ncpus)
        for i in range(len(phases_to_evaluate)):
            # we will use the uid_to_phase_ind create above to be able
            # to map results of parmap to self.phases
            ind = self.uid_to_phase_ind[phases_to_evaluate[i].description]
            self.phases[ind].stability = _result_list2[i]


    def _multiproc_help1(self, p):
        # For low e phases, we only eval stability if it doesn't exist
        if p.stability is None:
            try:
                p.stability = p.energy - self.gclp(p.unit_comp)[0]
            except:
                print(p)
                p.stability = np.nan
        return p.stability

    def _multiproc_help2(self, p):
        if p not in list(self.phase_dict.values()):
            if p.name in self.phase_dict:
                p.stability = p.energy - self.phase_dict[p.name].energy + self.phase_dict[p.name].stability
            else:
                try:
                    p.stability = p.energy - self.gclp(p.unit_comp)[0]
                except:
                    print(p)
                    p.stability = np.nan
        return p.stability


def fun(f, q_in, q_out):
    while True:
        i, x = q_in.get()
        if i is None:
            break
        q_out.put((i, f(x)))


def parmap(f, X, nprocs=multiprocessing.cpu_count()):
    q_in = multiprocessing.Queue(1)
    q_out = multiprocessing.Queue()

    proc = [multiprocessing.Process(target=fun, args=(f, q_in, q_out))
            for _ in range(nprocs)]
    for p in proc:
        p.daemon = True
        p.start()

    sent = [q_in.put((i, x)) for i, x in enumerate(X)]
    [q_in.put((None, None)) for _ in range(nprocs)]
    res = [q_out.get() for _ in range(len(sent))]

    [p.join() for p in proc]

    return [x for i, x in sorted(res)]


def update_run_w_structure(folder, hull_distance=0.2):
    """
    Updates a campaign grouped in directories with structure analysis

    """
    with cd(folder):
        required_files = ["seed_data.pickle"]
        if os.path.isfile("error.json"):
            error = loadfn("error.json")
            print("{} ERROR: {}".format(folder, error))

        if not all([os.path.isfile(fn) for fn in required_files]):
            print("{} ERROR: no seed data, no analysis to be done")
        else:
            iteration = -1
            jobs = {}
            while True:
                if os.path.isdir(str(iteration)):
                    jobs.update(loadfn(os.path.join(
                        str(iteration), '_exp_raw_results.json')))
                    iteration += 1
                else:
                    break
            with open("seed_data.pickle", "rb") as f:
                df = pickle.load(f)

            all_ids = loadfn("consumed_candidates.json")
            st_a = AnalyzeStability(df=df, hull_distance=hull_distance)
            _, stablities_of_discovered = st_a.analyze(df, all_ids, all_ids)

            # Having calculated stabilities again, we plot the overall hull.
            st_a.present(df, all_ids, all_ids, filename="hull_finalized.png",
                         finalize=True, save_hull_distance=True)

            stable_discovered = list(itertools.compress(
                all_ids, stablities_of_discovered))
            s_a = AnalyzeStructures()
            s_a.analyze_vaspqmpy_jobs(jobs, against_icsd=True, use_energies=True)
            unique_s_dict = {}
            for i in range(len(s_a.structures)):
                if s_a.structure_is_unique[i] and \
                        (s_a.structure_ids[i] in stable_discovered):
                    unique_s_dict[s_a.structure_ids[i]] = s_a.structures[i]

            with open("discovered_unique_structures.json", "w") as f:
                json.dump(dict([(k, s.as_dict())
                                for k, s in unique_s_dict.items()]), f)

            with open('structure_report.log', "w") as f:
                f.write("consumed discovery unique_discovery duplicate in_icsd \n")
                f.write(str(len(all_ids)) + ' ' +
                        str(len(stable_discovered)) + ' ' +
                        str(len(unique_s_dict)) + ' '
                        + str(len(s_a.structures) - sum(s_a._not_duplicate)) + ' '
                        + str(sum([not i for i in s_a._icsd_filter])))
