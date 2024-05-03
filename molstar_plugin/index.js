molstar.Viewer.create('app', {
    layoutIsExpanded: false,
    layoutShowControls: false,
    layoutShowRemoteState: false,
    layoutShowSequence: true,
    layoutShowLog: false,
    layoutShowLeftPanel: true,
    viewportShowExpand: false,
    viewportShowSelectionMode: false,
    viewportShowAnimation: false,
    pdbProvider: 'rcsb',
    emdbProvider: 'rcsb',
}).then(function (viewer) {
    viewer.loadPdb('148l');
});
// Attempt 1
// this.plugin.build().to(refToVisual).update(StateTransforms.Representation.StructureRepresentation3D, old => {
//     old.type.params.aromaticBonds = true;
// }).commit();
// Attempt 2
// import { DefaultPluginUISpec, PluginUISpec } from './molstar/lib/mol-plugin-ui/spec';
// import { createPluginUI } from './molstar/lib/mol-plugin-ui';
// import { renderReact18 } from './molstar/lib/mol-plugin-ui/react18';
// import { PluginConfig } from './molstar/lib/mol-plugin/config';
// const MySpec: PluginUISpec = {
//     ...DefaultPluginUISpec(),
//     config: [
//         [PluginConfig.VolumeStreaming.Enabled, false]
//     ]
// }
// async function createPlugin(parent: HTMLElement) {
//     const plugin = await createPluginUI({
//       target: parent,
//       spec: MySpec,
//       render: renderReact18
//     });
//     const data = await plugin.builders.data.download({ url: '...' }, { state: { isGhost: true } });
//     const trajectory = await plugin.builders.structure.parseTrajectory(data, format);
//     await this.plugin.builders.structure.hierarchy.applyPreset(trajectory, 'default');
//     return plugin;
// }
// createPlugin(document.getElementById('app')!); // app is a <div> element with position: relative
// Attempt 3
// const MyLabels3D = CreateTransformer({
//     name: 'my-labels-3d',
//     display: 'My Labels',
//     from: PluginStateObject.Molecule.Structure,
//     to: PluginStateObject.Shape.Representation3D,
//     params: {
//         // custom prams
//         ...LabelParams,
//     },
// })({
//     apply({ a, params }, plugin: PluginContext) {
//         return Task.create('Labels', async (ctx) => {
//             const data: LabelData = <create the object>; // access the custom property or pass the labels as params of the transform
//             // createIndexLabelData(a.data, params.selection);
//             const repr = LabelRepresentation(
//                 {
//                     webgl: plugin.canvas3d?.webgl,
//                     ...plugin.representation.structure.themes,
//                 },
//                 () => LabelParams
//             );
//             await repr.createOrUpdate(params, data).runInContext(ctx);
//             repr.setState({ pickable: false });
//             return new PluginStateObject.Shape.Representation3D({ repr, source: a }, { label: `Label` });
//         });
//     },
//     update({ a, b, newParams }) {
//         return Task.create('Labels', async (ctx) => {
//             const data: LabelData = <updated labels>;
//             await b.data.repr.createOrUpdate(newParams, data).runInContext(ctx);
//             return StateTransformer.UpdateResult.Updated;
//         });
//     },
// });
// /// .....
// await this.plugin.build().to(structureSelector).apply(MyLabels3D).commit();
// Attempt 4
// const data = await this.plugin.builders.data.download({ url });
// const trajectory = await this.plugin.builders.structure.parseTrajectory(data, format);
// const model = await this.plugin.builders.structure.createModel(trajectory);
// const structure = await this.plugin.builders.structure.createStructure(model);
// const components = {
//     polymer: await this.plugin.builders.structure.tryCreateComponentStatic(structure, 'polymer'),
//     ligand: await this.plugin.builders.structure.tryCreateComponentStatic(structure, 'ligand'),
//     water: await this.plugin.builders.structure.tryCreateComponentStatic(structure, 'water'),
// };
// const builder = this.plugin.builders.structure.representation;
// const update = this.plugin.build();
// if (components.polymer) builder.buildRepresentation(update, components.polymer, { type: 'gaussian-surface', typeParams: { alpha: 0.51 } }, { tag: 'polymer' });
// if (components.ligand) builder.buildRepresentation(update, components.ligand, { type: 'ball-and-stick' }, { tag: 'ligand' });
// if (components.water) builder.buildRepresentation(update, components.water, { type: 'ball-and-stick', typeParams: { alpha: 0.6 } }, { tag: 'water' });
// await update.commit();
// Attempt 5
// import { DefaultPluginSpec, PluginSpec } from './molstar/lib/mol-plugin/spec';
// import { PluginContext  } from './molstar/lib/mol-plugin/context';
// import { PluginConfig } from './molstar/lib/mol-plugin/config';
// const MySpec: PluginSpec = {
//     ...DefaultPluginSpec(),
//     config: [
//         [PluginConfig.VolumeStreaming.Enabled, false]
//     ]
// }
// async function init() {
//     const plugin = new PluginContext(MySpec);
//     await plugin.init();
//     const canvas = <HTMLCanvasElement> document.getElementById('molstar-canvas');
//     const parent = <HTMLDivElement> document.getElementById('molstar-parent');
//     if (!plugin.initViewer(canvas, parent)) {
//         console.error('Failed to init Mol*');
//         return;
//     }
//     // Example url:"https://files.rcsb.org/download/3j7z.pdb" 
//     // Example url:"https://files.rcsb.org/download/5AFI.cif" 
//     const data = await plugin.builders.data.download({ url: '...' }, { state: { isGhost: true } });
//     const format = 'pdb'
//     const trajectory = await plugin.builders.structure.parseTrajectory(data, format); //format is 'mmcif' or 'pdb' etc.
//     await plugin.builders.structure.hierarchy.applyPreset(trajectory, 'default');
// }
