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
    /**
     * Take a submitted pdb file from localStorage, display it in the molstar window, and add visualizations to indicate blobs.
     * 
     * @remarks
     * This function manipulates the molstar viewer and will not work if the molstar package is not properly installed.
     * See https://molstar.org/ and the associated documentation for more details.
     * 
     * @param plugin - plugin object generated by molstar representing the display window.
     */

    plugin.clear()
    let contentString = localStorage.getItem('pdb_file');
    // localStorage.removeItem('pdb_file')
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
    let shift = localStorage.getItem('pdbShift')

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
                tempHArray.push(blobIndex + Number(shift))
            }
            else if (blobArray[i] == 'h') {
                h_arr.push(tempHArray)
            }
            else if (blobArray[i] == 'p') {
                p_arr.push(blobIndex + Number(shift))
            }
            else if (blobArray[i] == 's') {
                s_arr.push(blobIndex+ Number(shift))
            };
        };
    };

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
    };

    for (var val_s of s_arr) {
        const sel = MS.struct.generator.atomGroups({
        'residue-test': MS.core.rel.eq([MS.struct.atomProperty.macromolecular.label_seq_id(), val_s]),
    })
    update.to(structure)
    .apply(StateTransforms.Model.StructureSelectionFromExpression, { label: 'Surroundings', expression: sel })
        .apply(StateTransforms.Representation.StructureRepresentation3D, createStructureRepresentationParams(plugin, structure.data, {
            type: 'cartoon',
            color: 'uniform',
            colorParams: { value: Color(0x66ff00) },
            typeParams: { alpha: 1.0}
        }));
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
    };

    update.commit();
};

async function createPlugin(parent: HTMLElement) {
    /**
     * Create a molstar window plugin instance.
     * 
     * @remarks
     * The plugin variable is used for both the loadPDB function and createBlobRepresentation
     * 
     * @param - parent (HTML element), the associated element on the webpage that contains the molstar window
     * 
     */
    
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

    setTimeout(() => {
        createBlobRepresentation(plugin)
        }, 1000);

    let elementsArray = document.querySelectorAll('.mutatebox,#snp_id,#residue_type,#domain_threshold_user_box,#domain_threshold_user_slider,#cutoff_user_box,#cutoff_user_slider,.checkbox,#hydro_scales')
    elementsArray.forEach(function(elem) {
        elem.addEventListener('change', function() {
        setTimeout(() => {
        createBlobRepresentation(plugin)
        }, 1000)});
    });
};

createPlugin(document.getElementById('app')!); // app is a <div> element with position: relativeE