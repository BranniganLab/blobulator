import { DefaultPluginUISpec, PluginUISpec } from '../../node_modules/molstar/lib/mol-plugin-ui/spec';
import { createPluginUI } from '../../node_modules/molstar/lib/mol-plugin-ui';
import { renderReact18 } from '../../node_modules/molstar/lib/mol-plugin-ui/react18';
import { PluginConfig } from '../../node_modules/molstar/lib/mol-plugin/config';

import { MolScriptBuilder as MS, MolScriptBuilder } from '../../node_modules/molstar/lib/mol-script/language/builder';
import { Color } from '../../node_modules/molstar/lib/mol-util/color';

import { StateTransforms } from '../../node_modules/molstar/lib/mol-plugin-state/transforms';
import { createStructureRepresentationParams } from '../../node_modules/molstar/lib/mol-plugin-state/helpers/structure-representation-params'


const MySpec: PluginUISpec = {
    ...DefaultPluginUISpec(),
    config: [
        [PluginConfig.VolumeStreaming.Enabled, false]
    ]
}

async function createBlobRepresentation(plugin) {
    let contentString = localStorage.getItem('pdb_file');
    localStorage.removeItem('pdb_file')
    const data = await plugin.builders.data.rawData({data: contentString})
    const trajectory = await plugin.builders.structure.parseTrajectory(data, 'pdb');

    const model = await plugin.builders.structure.createModel(trajectory);
    const structure = await plugin.builders.structure.createStructure(model);

    const components = {
    polymer: await plugin.builders.structure.tryCreateComponentStatic(structure, 'polymer'),
    };

    const builder = plugin.builders.structure.representation;
    const update = plugin.build();

    builder.buildRepresentation(update, components.polymer, { type: 'cartoon', typeParams: { alpha: 0.0 }, color : 'uniform', colorParams: { value: Color(0x1A5653) } }, { tag: 'polymer' });
    
    let blobString = localStorage.getItem('blobSeq')
    let blobArray = blobString?.split(',')
    var p_arr: number[] = []
    var tempHArray: number[] = []
    var h_arr: number[][] = []
    var s_arr: number[] = []

    if (typeof blobArray != 'undefined') {
        for (let i = 0; i < blobArray.length; i++) {
            var blobIndex = i + 1
            var nextArrayIndex = i + 1
            if (blobArray[i] == 'h' && blobArray[nextArrayIndex] != 'p' && blobArray[nextArrayIndex] != 's') {
                tempHArray.push(blobIndex)
            }
            else if (blobArray[i] == 'h') {
                h_arr.push(tempHArray)
            }
            else if (blobArray[i] == 'p') {
                p_arr.push(blobIndex)
            }
            else if (blobArray[i] == 's') {
                s_arr.push(blobIndex)
            };
        };
    };

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

    };

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
    };
}

async function createPlugin(parent: HTMLElement) {
    const defaultSpec = DefaultPluginUISpec();
    const plugin = await createPluginUI({
      target: parent,
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

    createBlobRepresentation(plugin);
};

createPlugin(document.getElementById('app')!); // app is a <div> element with position: relativeE

const hydroSlider = document.getElementById("cutoff_user_slider")
hydroSlider?.addEventListener("change", () => {
    createPlugin(document.getElementById('app')!)
});