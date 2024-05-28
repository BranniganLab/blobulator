import { DefaultPluginUISpec, PluginUISpec } from '../node_modules/molstar/lib/mol-plugin-ui/spec';
import { createPluginUI } from '../node_modules/molstar/lib/mol-plugin-ui';
import { renderReact18 } from '../node_modules/molstar/lib/mol-plugin-ui/react18';
import { PluginConfig } from '../node_modules/molstar/lib/mol-plugin/config';
import { compileIdListSelection } from 'molstar/lib/mol-script/util/id-list';

import { MolScriptBuilder as MS, MolScriptBuilder } from '../node_modules/molstar/lib/mol-script/language/builder';
import { Expression } from '../node_modules/molstar/lib/mol-script/language/expression';
import {  StructureSelectionQuery } from '../node_modules/molstar/lib/mol-plugin-state/helpers/structure-selection-query';
import {
  Structure,
  StructureProperties,
} from "../node_modules/molstar/lib/mol-model/structure";
import { Script } from '../node_modules/molstar/lib/mol-script/script';
import { Color } from '../node_modules/molstar/lib/mol-util/color';
import { ColorNames } from '../node_modules/molstar/lib/mol-util/color/names'

import { StateTransforms } from '../node_modules/molstar/lib/mol-plugin-state/transforms';
import { createStructureRepresentationParams } from '../node_modules/molstar/lib/mol-plugin-state/helpers/structure-representation-params'

const MySpec: PluginUISpec = {
    ...DefaultPluginUISpec(),
    config: [
        [PluginConfig.VolumeStreaming.Enabled, false]
    ]
}

async function createPlugin(parent: HTMLElement) {
    const plugin = await createPluginUI({
      target: parent,
      spec: MySpec,
      render: renderReact18
    });

    const data = await plugin.builders.data.download({ url: "https://files.rcsb.org/download/1dpx.pdb" }, { state: { isGhost: true } });
    const trajectory = await plugin.builders.structure.parseTrajectory(data, 'pdb');
    // await plugin.builders.structure.hierarchy.applyPreset(trajectory, 'default');

    const model = await plugin.builders.structure.createModel(trajectory);
    const structure = await plugin.builders.structure.createStructure(model);

    const components = {
    polymer: await plugin.builders.structure.tryCreateComponentStatic(structure, 'polymer'),
    };

    const builder = plugin.builders.structure.representation;
    const update = plugin.build();

    // // Select residue 124 of chain A and convert to Loci
    // const Q = MolScriptBuilder;
    // var sel = Script.getStructureSelection(Q => Q.struct.generator.atomGroups({
    //                 "residue-test": Q.core.rel.eq([Q.struct.atomProperty.macromolecular.label_seq_id(), 11]),
    //               }), objdata)

    // const components = {
    //     blob: await plugin.builders.structure.tryCreateComponentFromSelection(structure, sel, "residue-test")
    // }

    // builder.buildRepresentation(update, components.polymer, { type: 'gaussian-surface', typeParams: { alpha: 0.51 }, color : 'uniform', colorParams: { value: Color(0x073763) } }, { tag: 'polymer' });
    builder.buildRepresentation(update, components.polymer, { type: 'cartoon', typeParams: { alpha: 1.0 }, color : 'uniform', colorParams: { value: Color(0xFFA500) } }, { tag: 'polymer' });
    // await update.commit();

        const sel = MS.struct.generator.atomGroups({
        'residue-test': MS.core.rel.eq([MS.struct.atomProperty.macromolecular.label_seq_id(), 15]),
    });


    update.to(structure)
        .apply(StateTransforms.Model.StructureSelectionFromExpression, { label: 'Surroundings', expression: sel })
        .apply(StateTransforms.Representation.StructureRepresentation3D, createStructureRepresentationParams(plugin, structure.data, {
            type: 'gaussian-surface',
            color: 'uniform',
            colorParams: { value: Color(0x0096FF) }
        }));

    await update.commit();


    return plugin;
}

createPlugin(document.getElementById('app')!); // app is a <div> element with position: relative