import { DefaultPluginUISpec, PluginUISpec } from 'molstar/lib/mol-plugin-ui/spec';
import { createPluginUI } from 'molstar/lib/mol-plugin-ui';
import { renderReact18 } from 'molstar/lib/mol-plugin-ui/react18';
import { PluginConfig } from 'molstar/lib/mol-plugin/config';

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

    const data = await plugin.builders.data.download({ url: '...' }, { state: { isGhost: true } });
    const trajectory = await plugin.builders.structure.parseTrajectory(data, format);
    await this.plugin.builders.structure.hierarchy.applyPreset(trajectory, 'default');

    return plugin;
}

createPlugin(document.getElementById('app')!); // app is a <div> element with position: relative