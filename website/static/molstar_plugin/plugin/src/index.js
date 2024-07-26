"use strict";
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
Object.defineProperty(exports, "__esModule", { value: true });
var spec_1 = require("../../node_modules/molstar/lib/mol-plugin-ui/spec");
var mol_plugin_ui_1 = require("../../node_modules/molstar/lib/mol-plugin-ui");
var react18_1 = require("../../node_modules/molstar/lib/mol-plugin-ui/react18");
var config_1 = require("../../node_modules/molstar/lib/mol-plugin/config");
var builder_1 = require("../../node_modules/molstar/lib/mol-script/language/builder");
var color_1 = require("../../node_modules/molstar/lib/mol-util/color");
var transforms_1 = require("../../node_modules/molstar/lib/mol-plugin-state/transforms");
var structure_representation_params_1 = require("../../node_modules/molstar/lib/mol-plugin-state/helpers/structure-representation-params");
var MySpec = __assign(__assign({}, (0, spec_1.DefaultPluginUISpec)()), { config: [
        [config_1.PluginConfig.VolumeStreaming.Enabled, false],
        // [PluginConfig.Viewport.ShowExpand, false],
        // [PluginConfig.Viewport.ShowControls, false],
        // [PluginConfig.Viewport.ShowSettings, false],
        // [PluginConfig.Viewport.ShowAnimation, false],
    ] });
function createPlugin(parent) {
    return __awaiter(this, void 0, void 0, function () {
        var defaultSpec, plugin, file, contentString, data, trajectory, model, structure, components, builder, update, p_arr, h_arr, s_arr, _i, h_arr_1, val_h, sel, _a, p_arr_1, val_p, sel, _b, s_arr_1, val_s, sel;
        var _c;
        return __generator(this, function (_d) {
            switch (_d.label) {
                case 0:
                    defaultSpec = (0, spec_1.DefaultPluginUISpec)();
                    return [4 /*yield*/, (0, mol_plugin_ui_1.createPluginUI)({
                            target: parent,
                            // spec: MySpec,
                            // render: renderReact18
                            render: react18_1.renderReact18,
                            spec: __assign(__assign({}, defaultSpec), { layout: {
                                    initial: {
                                        isExpanded: false,
                                        showControls: false
                                    },
                                }, components: {
                                    controls: { left: 'none', right: 'none', top: 'none', bottom: 'none' },
                                }, canvas3d: {
                                    camera: {
                                        helper: { axes: { name: 'off', params: {} } }
                                    }
                                }, config: [
                                    [config_1.PluginConfig.Viewport.ShowExpand, false],
                                    [config_1.PluginConfig.Viewport.ShowControls, false],
                                    [config_1.PluginConfig.Viewport.ShowSelectionMode, false],
                                    [config_1.PluginConfig.Viewport.ShowAnimation, false],
                                ] })
                        })];
                case 1:
                    plugin = _d.sent();
                    file = jQuery.get('pdb_files/current.pdb');
                    console.log(file);
                    contentString = JSON.stringify(file);
                    console.log(contentString);
                    return [4 /*yield*/, plugin.builders.data.rawData({ data: contentString })];
                case 2:
                    data = _d.sent();
                    return [4 /*yield*/, plugin.builders.structure.parseTrajectory(data, 'pdb')];
                case 3:
                    trajectory = _d.sent();
                    return [4 /*yield*/, plugin.builders.structure.createModel(trajectory)];
                case 4:
                    model = _d.sent();
                    return [4 /*yield*/, plugin.builders.structure.createStructure(model)];
                case 5:
                    structure = _d.sent();
                    _c = {};
                    return [4 /*yield*/, plugin.builders.structure.tryCreateComponentStatic(structure, 'polymer')];
                case 6:
                    components = (_c.polymer = _d.sent(),
                        _c);
                    builder = plugin.builders.structure.representation;
                    update = plugin.build();
                    builder.buildRepresentation(update, components.polymer, { type: 'cartoon', typeParams: { alpha: 0.0 }, color: 'uniform', colorParams: { value: (0, color_1.Color)(0xFFA500) } }, { tag: 'polymer' });
                    p_arr = [10, 11, 12, 13, 20, 21, 22, 23, 24, 32, 33, 34, 35, 36, 42, 43, 44, 45, 46, 57, 58, 59, 60, 61, 62, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140];
                    h_arr = [[1, 2, 3, 4, 5, 6, 7, 8, 9], [14, 15, 16, 17, 18, 19], [25, 26, 27, 28, 29, 30, 31], [37, 38, 39, 40, 41], [47, 48, 49, 50, 51, 52, 53, 54, 55, 56], [63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78], [81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96]];
                    s_arr = [79, 80];
                    for (_i = 0, h_arr_1 = h_arr; _i < h_arr_1.length; _i++) {
                        val_h = h_arr_1[_i];
                        sel = builder_1.MolScriptBuilder.struct.generator.atomGroups({
                            'residue-test': builder_1.MolScriptBuilder.core.set.has([builder_1.MolScriptBuilder.set.apply(builder_1.MolScriptBuilder, val_h), builder_1.MolScriptBuilder.ammp('label_seq_id')])
                        });
                        update.to(structure)
                            .apply(transforms_1.StateTransforms.Model.StructureSelectionFromExpression, { label: 'Surroundings', expression: sel })
                            .apply(transforms_1.StateTransforms.Representation.StructureRepresentation3D, (0, structure_representation_params_1.createStructureRepresentationParams)(plugin, structure.data, {
                            type: 'gaussian-surface',
                            color: 'uniform',
                            colorParams: { value: (0, color_1.Color)(0x0096FF) },
                            typeParams: { alpha: 1.0 }
                        }));
                        update.commit();
                    }
                    for (_a = 0, p_arr_1 = p_arr; _a < p_arr_1.length; _a++) {
                        val_p = p_arr_1[_a];
                        sel = builder_1.MolScriptBuilder.struct.generator.atomGroups({
                            'residue-test': builder_1.MolScriptBuilder.core.rel.eq([builder_1.MolScriptBuilder.struct.atomProperty.macromolecular.label_seq_id(), val_p]),
                        });
                        update.to(structure)
                            .apply(transforms_1.StateTransforms.Model.StructureSelectionFromExpression, { label: 'Surroundings', expression: sel })
                            .apply(transforms_1.StateTransforms.Representation.StructureRepresentation3D, (0, structure_representation_params_1.createStructureRepresentationParams)(plugin, structure.data, {
                            type: 'cartoon',
                            color: 'uniform',
                            colorParams: { value: (0, color_1.Color)(0xFFA500) },
                            typeParams: { alpha: 1.0 }
                        }));
                        update.commit();
                    }
                    for (_b = 0, s_arr_1 = s_arr; _b < s_arr_1.length; _b++) {
                        val_s = s_arr_1[_b];
                        sel = builder_1.MolScriptBuilder.struct.generator.atomGroups({
                            'residue-test': builder_1.MolScriptBuilder.core.rel.eq([builder_1.MolScriptBuilder.struct.atomProperty.macromolecular.label_seq_id(), val_s]),
                        });
                        update.to(structure)
                            .apply(transforms_1.StateTransforms.Model.StructureSelectionFromExpression, { label: 'Surroundings', expression: sel })
                            .apply(transforms_1.StateTransforms.Representation.StructureRepresentation3D, (0, structure_representation_params_1.createStructureRepresentationParams)(plugin, structure.data, {
                            type: 'cartoon',
                            color: 'uniform',
                            colorParams: { value: (0, color_1.Color)(0x00FF00) },
                            typeParams: { alpha: 1.0 }
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
                    return [2 /*return*/, plugin];
            }
        });
    });
}
createPlugin(document.getElementById('app')); // app is a <div> element with position: relative
