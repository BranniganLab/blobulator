
import { DefaultPluginUISpec, PluginUISpec } from '../../node_modules/molstar/lib/mol-plugin-ui/spec';
import { createPluginUI } from '../../node_modules/molstar/lib/mol-plugin-ui';
import { renderReact18 } from '../../node_modules/molstar/lib/mol-plugin-ui/react18';
import { PluginConfig } from '../../node_modules/molstar/lib/mol-plugin/config';
import { PluginContext } from '../../node_modules/molstar/lib/mol-plugin/context'

import { MolScriptBuilder as MS, MolScriptBuilder } from '../../node_modules/molstar/lib/mol-script/language/builder';
import { Expression } from '../../node_modules/molstar/lib/mol-script/language/expression';
import {  StructureSelectionQuery } from '../../node_modules/molstar/lib/mol-plugin-state/helpers/structure-selection-query';
import {
  Structure,
  StructureProperties,
} from "../../node_modules/molstar/lib/mol-model/structure";
import { Script } from '../../node_modules/molstar/lib/mol-script/script';
import { Color } from '../../node_modules/molstar/lib/mol-util/color';
import { ColorNames } from '../../node_modules/molstar/lib/mol-util/color/names'

import { StateTransforms } from '../../node_modules/molstar/lib/mol-plugin-state/transforms';
import { createStructureRepresentationParams } from '../../node_modules/molstar/lib/mol-plugin-state/helpers/structure-representation-params'

const MySpec: PluginUISpec = {
    ...DefaultPluginUISpec(),
    config: [
        [PluginConfig.VolumeStreaming.Enabled, false],
        // [PluginConfig.Viewport.ShowExpand, false],
        // [PluginConfig.Viewport.ShowControls, false],
        // [PluginConfig.Viewport.ShowSettings, false],
        // [PluginConfig.Viewport.ShowAnimation, false],
    ]
}

async function createPlugin(parent: HTMLElement) {
    const defaultSpec = DefaultPluginUISpec();
    const plugin = await createPluginUI({
      target: parent,
      // spec: MySpec,
      // render: renderReact18
      render: renderReact18,
            spec: {
                ...defaultSpec,
                layout: {
                    initial: {
                        isExpanded: false,
                        showControls: false
                    },
                },
                components: {
                    controls: { left: 'none', right: 'none', top: 'none', bottom: 'none' },
                },
                canvas3d: {
                    camera: {
                        helper: { axes: { name: 'off', params: {} } }
                    }
                },
                config: [
                    [PluginConfig.Viewport.ShowExpand, false],
                    [PluginConfig.Viewport.ShowControls, false],
                    [PluginConfig.Viewport.ShowSelectionMode, false],
                    [PluginConfig.Viewport.ShowAnimation, false],
                ]
            }
    });


    const data = await plugin.builders.data.download({ url: "https://files.rcsb.org/download/1xq8.pdb" }, { state: { isGhost: true } });
    const trajectory = await plugin.builders.structure.parseTrajectory(data, 'pdb');
    // await plugin.builders.structure.hierarchy.applyPreset(trajectory, 'default');

    const model = await plugin.builders.structure.createModel(trajectory);
    const structure = await plugin.builders.structure.createStructure(model);

    const components = {
    polymer: await plugin.builders.structure.tryCreateComponentStatic(structure, 'polymer'),
    };

    const builder = plugin.builders.structure.representation;
    const update = plugin.build();

    builder.buildRepresentation(update, components.polymer, { type: 'cartoon', typeParams: { alpha: 0.0 }, color : 'uniform', colorParams: { value: Color(0xFFA500) } }, { tag: 'polymer' });
    // await update.commit();

    let p_arr = [10, 11, 12, 13,  20, 21, 22, 23, 24, , 32, 33, 34, 35, 36, 42, 43, 44, 45, 46, 57, 58, 59, 60, 61, 62, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140]
    let h_arr = [[1, 2, 3, 4, 5, 6, 7, 8, 9], [14, 15, 16, 17, 18, 19], [25, 26, 27, 28, 29, 30, 31], [37, 38, 39, 40, 41], [47, 48, 49, 50, 51, 52, 53, 54, 55, 56], [63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78], [81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96]]
    let s_arr = [79, 80]

    for (var val_h of h_arr) {
        const sel = MS.struct.generator.atomGroups({
            'residue-test': MS.core.set.has([MS.set(...val_h), MS.ammp('label_seq_id')])
        });
        update.to(structure)
        .apply(StateTransforms.Model.StructureSelectionFromExpression, { label: 'Surroundings', expression: sel })
        .apply(StateTransforms.Representation.StructureRepresentation3D, createStructureRepresentationParams(plugin, structure.data, {
            type: 'gaussian-surface',
            color: 'uniform',
            colorParams: { value: Color(0x0096FF) },
            typeParams: { alpha: 1.0}
        }));

    update.commit();

    }

    for (var val_p of p_arr) {
        const sel = MS.struct.generator.atomGroups({
        'residue-test': MS.core.rel.eq([MS.struct.atomProperty.macromolecular.label_seq_id(), val_p]),
    });
        update.to(structure)
        .apply(StateTransforms.Model.StructureSelectionFromExpression, { label: 'Surroundings', expression: sel })
        .apply(StateTransforms.Representation.StructureRepresentation3D, createStructureRepresentationParams(plugin, structure.data, {
            type: 'cartoon',
            color: 'uniform',
            colorParams: { value: Color(0xFFA500) },
            typeParams: { alpha: 1.0}
        }));

    update.commit();

    }

    for (var val_s of s_arr) {
        const sel = MS.struct.generator.atomGroups({
        'residue-test': MS.core.rel.eq([MS.struct.atomProperty.macromolecular.label_seq_id(), val_s]),
    });
        update.to(structure)
        .apply(StateTransforms.Model.StructureSelectionFromExpression, { label: 'Surroundings', expression: sel })
        .apply(StateTransforms.Representation.StructureRepresentation3D, createStructureRepresentationParams(plugin, structure.data, {
            type: 'cartoon',
            color: 'uniform',
            colorParams: { value: Color(0x00FF00) },
            typeParams: { alpha: 1.0}
        }));

    update.commit();

    }


        

    // update.to(structure)
    //     .apply(StateTransforms.Model.StructureSelectionFromExpression, { label: 'Surroundings', expression: sel })
    //     .apply(StateTransforms.Representation.StructureRepresentation3D, createStructureRepresentationParams(plugin, structure.data, {
    //         type: 'gaussian-surface',
    //         color: 'uniform',
    //         colorParams: { value: Color(0x0096FF) }
    //     }));

    // await update.commit();


    return plugin;
}

createPlugin(document.getElementById('app')!); // app is a <div> element with position: relative
