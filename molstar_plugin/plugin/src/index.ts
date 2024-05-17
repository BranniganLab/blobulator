import { DefaultPluginUISpec, PluginUISpec } from '../node_modules/molstar/lib/mol-plugin-ui/spec';
import { createPluginUI } from '../node_modules/molstar/lib/mol-plugin-ui';
import { renderReact18 } from '../node_modules/molstar/lib/mol-plugin-ui/react18';
import { PluginConfig } from '../node_modules/molstar/lib/mol-plugin/config';
import { compileIdListSelection } from 'molstar/lib/mol-script/util/id-list';

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
    await plugin.builders.structure.hierarchy.applyPreset(trajectory, 'default');

    const model = await plugin.builders.structure.createModel(trajectory);
    const structure = await plugin.builders.structure.createStructure(model);

    const components = {
    polymer: await plugin.builders.structure.tryCreateComponentStatic(structure, 'polymer'),
    };

    const builder = plugin.builders.structure.representation;
    const update = plugin.build();

    builder.buildRepresentation(update, components.polymer, { type: 'gaussian-surface', typeParams: { alpha: 0.51 } }, { tag: 'polymer' });
    await update.commit();


    return plugin;
}

createPlugin(document.getElementById('app')!); // app is a <div> element with position: relative