"""
Test cases for tree sequences.
"""
from __future__ import print_function
from __future__ import division

import pyslim
import tskit
import msprime
import tests
import unittest
import random
import os
import numpy as np


class TestRecapitation(tests.PyslimTestCase):
    '''
    Tests for recapitation.
    '''

    def check_recap_consistency(self, ts, recap,
                                keep_first_generation):
        self.assertEqual(ts.slim_generation, recap.slim_generation)
        self.assertTrue(all(tree.num_roots == 1 for tree in recap.trees()))

        ts_samples = list(ts.samples())
        for u in recap.samples():
            n1 = recap.node(u)
            self.assertGreaterEqual(n1.individual, 0)
            i1 = recap.individual(n1.individual)
            firstgen = ((pyslim.INDIVIDUAL_FIRST_GEN & i1.flags) > 0)
            remembered = ((pyslim.INDIVIDUAL_REMEMBERED & i1.flags) > 0)
            alive = ((pyslim.INDIVIDUAL_ALIVE & i1.flags) > 0)
            self.assertTrue(alive or remembered or (firstgen and keep_first_generation))
            self.assertTrue((keep_first_generation and firstgen) or (u in ts_samples))
            n2 = ts.node(u)
            self.assertEqual(n1.time, n2.time)
            self.assertEqual(n1.individual, n2.individual)
            recap_flags = n1.flags
            if keep_first_generation and firstgen and not remembered and not alive:
                recap_flags = (recap_flags & ~msprime.NODE_IS_SAMPLE)
            self.assertEqual(recap_flags, n2.flags)
            self.assertEqual(n1.metadata, n2.metadata)
            self.assertEqual(n1.population, n2.population)
        self.assertLessEqual(ts.num_populations, recap.num_populations)
        for k in range(ts.num_populations):
            p1 = ts.population(k)
            p2 = recap.population(k)
            self.assertEqual(p1.metadata, p2.metadata)

    def test_recapitation(self):
        for ts in self.get_slim_examples():
            assert ts.num_populations == 2
            # if not we need migration rates
            for keep_first in [True, False]:
                recomb_rate = 1.0 / ts.sequence_length
                recap = ts.recapitate(recombination_rate = recomb_rate,
                                      keep_first_generation=keep_first)
                # there should be no new mutations
                self.assertEqual(ts.num_mutations, recap.num_mutations)
                self.assertEqual(ts.num_sites, recap.num_sites)
                self.assertListEqual(list(ts.tables.sites.position),
                                     list(recap.tables.sites.position))
                self.check_recap_consistency(ts, recap, keep_first)
                for t in recap.trees():
                    self.assertEqual(t.num_roots, 1)

                recap = ts.recapitate(recombination_rate = recomb_rate,
                                      Ne = 1e-6, keep_first_generation=keep_first)
                self.check_recap_consistency(ts, recap, keep_first)
                if ts.slim_generation < 200:
                    for t in recap.trees():
                        self.assertEqual(t.num_roots, 1)
                        self.assertAlmostEqual(recap.node(t.root).time, 
                                               recap.slim_generation, 
                                               delta = 1e-4)


class TestIndividualMetadata(tests.PyslimTestCase):
    # Tests for extra stuff related to Individuals.

    def test_individual_derived_info(self):
        for ts in self.get_slim_examples():
            for j, ind in enumerate(ts.individuals()):
                a = ts.tables.individuals.metadata_offset[j]
                b = ts.tables.individuals.metadata_offset[j+1]
                raw_md = ts.tables.individuals.metadata[a:b]
                md = pyslim.decode_individual(raw_md)
                self.assertEqual(ind.metadata, md)
                self.assertEqual(ts.individual(j).metadata, md)
                for n in ind.nodes:
                    self.assertEqual(ts.node(n).population, ind.population)
                    self.assertEqual(ts.node(n).time, ind.time)

    def test_individual_embellishments(self):
        # Test the individual additional information.
        for ts in self.get_slim_examples():
            is_wf = (ts.slim_provenance.model_type == "WF")
            for j, ind in enumerate(ts.individuals()):
                self.assertEqual(ts.individual_times[j], ind.time)
                if is_wf:
                    self.assertEqual(ts.individual_ages[j], 0)
                else:
                    self.assertEqual(ts.individual_ages[j], ind.metadata.age)
                self.assertEqual(ts.individual_populations[j], ind.population)
                self.assertArrayEqual(ts.individual_locations[j], ind.location)

    def test_first_gen(self):
        for ts in self.get_slim_examples():
            firstgen = ts.first_generation_individuals()
            firstgen_times = ts.individual_times[firstgen]
            self.assertEqual(len(set(firstgen_times)), 1)
            self.assertEqual(firstgen_times[0], np.max(ts.individual_times))
            for i in firstgen:
                self.assertGreaterEqual(ts.individual(i).flags & pyslim.INDIVIDUAL_FIRST_GEN, 0)

class TestNodeMetadata(tests.PyslimTestCase):
    '''
    Tests for extra stuff related to Nodes.
    '''

    def test_node_derived_info(self):
        for ts in self.get_slim_examples():
            for j, node in enumerate(ts.nodes()):
                a = ts.tables.nodes.metadata_offset[j]
                b = ts.tables.nodes.metadata_offset[j+1]
                raw_md = ts.tables.nodes.metadata[a:b]
                md = pyslim.decode_node(raw_md)
                self.assertEqual(node.metadata, md)
                self.assertEqual(ts.node(j).metadata, md)


class TestMutationMetadata(tests.PyslimTestCase):
    '''
    Tests for extra stuff related to Mutations.
    '''

    def test_mutation_derived_info(self):
        for ts in self.get_slim_examples():
            for j, mut in enumerate(ts.mutations()):
                a = ts.tables.mutations.metadata_offset[j]
                b = ts.tables.mutations.metadata_offset[j+1]
                raw_md = ts.tables.mutations.metadata[a:b]
                md = pyslim.decode_mutation(raw_md)
                self.assertEqual(mut.metadata, md)
                self.assertEqual(ts.mutation(j).metadata, md)

    def test_slim_time(self):
        # check that slim_times make sense
        for ts in self.get_slim_examples():
            # Mutation's slim_times are one less than the corresponding node's slim times
            # in WF models, but not in WF models, for some reason.
            is_wf = (ts.slim_provenance.model_type == "WF")
            for mut in ts.mutations():
                node_slim_time = ts.slim_generation - ts.node(mut.node).time
                mut_slim_time = max([u.slim_time for u in mut.metadata])
                self.assertGreaterEqual(node_slim_time, mut_slim_time)


class TestPopulationMetadata(tests.PyslimTestCase):
    '''
    Tests for extra stuff related to Populations.
    '''

    def test_population_derived_info(self):
        for ts in self.get_slim_examples():
            for j, pop in enumerate(ts.populations()):
                a = ts.tables.populations.metadata_offset[j]
                b = ts.tables.populations.metadata_offset[j+1]
                raw_md = ts.tables.populations.metadata[a:b]
                md = pyslim.decode_population(raw_md)
                self.assertEqual(pop.metadata, md)
                self.assertEqual(ts.population(j).metadata, md)


class TestEveryone(tests.PyslimTestCase):
    '''
    Test things we calculate from tree sequences where 
    everyone is remembered at all times.
    '''

    def test_alive_ages(self):
        for ts in self.get_slim_everyone_examples():
            is_WF = (ts.slim_provenance.model_type == "WF")
            ages_mat = np.zeros((ts.num_individuals, ts.slim_generation))
            alive_mat = np.zeros((ts.num_individuals, ts.slim_generation))
            alive_now = ts.individuals_alive_at(0)
            for time in range(ts.slim_generation):
                ages_mat[:, time] = ts.individual_ages_at(time)
                for j in ts.individuals_alive_at(time):
                    alive_mat[j, time] = 1

            for j, ind in enumerate(ts.individuals()):
                if is_WF:
                    age = 0
                else:
                    age = ind.metadata.age
                self.assertEqual(j in alive_now,
                                 ind.flags & pyslim.INDIVIDUAL_ALIVE > 0)
                self.assertEqual(sum(alive_mat[j, :]), 1 + age)
                self.assertEqual(alive_mat[j, int(ind.time)], 1)
                self.assertEqual(ages_mat[j, int(ind.time)], 0)
                for t in range(ts.slim_generation):
                    if t > ind.time:
                        self.assertTrue(np.isnan(ages_mat[j, t]))
                    if t == ind.time:
                        self.assertEqual(ages_mat[j, t], 0)
                if ind.time + 1 < ts.slim_generation:
                    self.assertEqual(alive_mat[j, int(ind.time + 1)], 0)


class TestSimplify(tests.PyslimTestCase):
    '''
    Our simplify() is just a wrapper around the tskit simplify.
    '''

    def test_simplify(self):
        for ts in self.get_slim_examples():
            sts = ts.simplify()
            self.assertEqual(ts.sequence_length, sts.sequence_length)
            self.assertEqual(type(ts), type(sts))
            self.assertEqual(sts.samples()[0], 0)    


class TestReferenceSequence(tests.PyslimTestCase):
    '''
    Test for operations involving the reference sequence
    '''

    def test_reference_sequence(self):
        for ts in self.get_slim_examples():
            mut_md = ts.mutation(0).metadata
            has_nucleotides = (mut_md[0].nucleotide >= 0)
            if not has_nucleotides:
                self.assertEqual(ts.reference_sequence, None)
            else:
                self.assertEqual(type(ts.reference_sequence), type(''))
                self.assertEqual(len(ts.reference_sequence), ts.sequence_length)
                for u in ts.reference_sequence:
                    self.assertTrue(u in pyslim.NUCLEOTIDES)
            sts = ts.simplify(ts.samples()[:2])
            self.assertEqual(sts.reference_sequence, ts.reference_sequence)

    def test_mutation_at_errors(self):
        for ts in self.get_slim_examples():
            u = ts.samples()[0]
            with self.assertRaises(ValueError):
                ts.mutation_at(-2, 3)
            with self.assertRaises(ValueError):
                ts.mutation_at(u, -3)
            with self.assertRaises(ValueError):
                ts.mutation_at(ts.num_nodes + 2, 3)
            with self.assertRaises(ValueError):
                ts.mutation_at(u, ts.sequence_length)

    def test_nucleotide_at_errors(self):
        for ts in self.get_slim_examples():
            u = ts.samples()[0]
            mut_md = ts.mutation(0).metadata
            has_nucleotides = (mut_md[0].nucleotide >= 0)
            if not has_nucleotides:
                with self.assertRaises(ValueError):
                    ts.nucleotide_at(u, 3)

    def test_mutation_at(self):
        for ts in self.get_slim_examples():
            for _ in range(100):
                node = random.randint(0, ts.num_nodes - 1)
                pos = random.randint(0, ts.sequence_length - 1)
                tree = ts.at(pos)
                parent = tree.parent(node)
                a = ts.mutation_at(node, pos)
                if parent == tskit.NULL:
                    self.assertEqual(a, tskit.NULL)
                else:
                    b = ts.mutation_at(parent, pos)
                    c = ts.mutation_at(node, pos, ts.node(parent).time)
                    self.assertEqual(b, c)
                    for k in np.where(node == ts.tables.mutations.node)[0]:
                        mut = ts.mutation(k)
                        if ts.site(mut.site).position == pos:
                            b = mut.id
                    self.assertEqual(a, b)

    def test_nucleotide_at(self):
        for ts in self.get_slim_examples():
            mut_md = ts.mutation(0).metadata
            has_nucleotides = (mut_md[0].nucleotide >= 0)
            if has_nucleotides:
                for _ in range(100):
                    node = random.randint(0, ts.num_nodes - 1)
                    pos = random.randint(0, ts.sequence_length - 1)
                    tree = ts.at(pos)
                    parent = tree.parent(node)
                    a = ts.nucleotide_at(node, pos)
                    if parent == tskit.NULL:
                        nuc = ts.reference_sequence[int(pos)]
                        self.assertEqual(a, pyslim.NUCLEOTIDES.index(nuc))
                    else:
                        b = ts.nucleotide_at(parent, pos)
                        c = ts.nucleotide_at(node, pos, ts.node(parent).time)
                        self.assertEqual(b, c)
                        for k in np.where(node == ts.tables.mutations.node)[0]:
                            mut = ts.mutation(k)
                            if ts.site(mut.site).position == pos:
                                b = mut.metadata[0].nucleotide
                        self.assertEqual(a, b)
