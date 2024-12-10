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
var spec_1 = require("@molstar-lib/mol-plugin-ui/spec");
var mol_plugin_ui_1 = require("@molstar-lib/mol-plugin-ui");
var react18_1 = require("@molstar-lib/mol-plugin-ui/react18");
var config_1 = require("@molstar-lib/mol-plugin/config");
var builder_1 = require("@molstar-lib/mol-script/language/builder");
var color_1 = require("@molstar-lib/mol-util/color");
var transforms_1 = require("@molstar-lib/mol-plugin-state/transforms");
var structure_representation_params_1 = require("@molstar-lib/mol-plugin-state/helpers/structure-representation-params");
var MySpec = __assign(__assign({}, (0, spec_1.DefaultPluginUISpec)()), { config: [
        [config_1.PluginConfig.VolumeStreaming.Enabled, false]
    ] });
function createBlobRepresentation(plugin) {
    return __awaiter(this, void 0, void 0, function () {
        var contentString, data, trajectory, model, structure, components, builder, update, blobString, blobArray, p_arr, tempHArray, h_arr, s_arr, i, blobIndex, nextArrayIndex, _i, h_arr_1, val_h, sel, _a, p_arr_1, val_p, sel, _b, s_arr_1, val_s, sel, _c, h_arr_2, val_h, sel_1;
        var _d;
        return __generator(this, function (_e) {
            switch (_e.label) {
                case 0:
                    plugin.clear();
                    contentString = localStorage.getItem('pdb_file');
                    return [4 /*yield*/, plugin.builders.data.rawData({ data: contentString })];
                case 1:
                    data = _e.sent();
                    return [4 /*yield*/, plugin.builders.structure.parseTrajectory(data, 'pdb')];
                case 2:
                    trajectory = _e.sent();
                    return [4 /*yield*/, plugin.builders.structure.createModel(trajectory)];
                case 3:
                    model = _e.sent();
                    return [4 /*yield*/, plugin.builders.structure.createStructure(model)];
                case 4:
                    structure = _e.sent();
                    _d = {};
                    return [4 /*yield*/, plugin.builders.structure.tryCreateComponentStatic(structure, 'polymer')];
                case 5:
                    components = (_d.polymer = _e.sent(),
                        _d);
                    builder = plugin.builders.structure.representation;
                    update = plugin.build();
                    builder.buildRepresentation(update, components.polymer, { type: 'cartoon', typeParams: { alpha: 0.0 }, color: 'uniform', colorParams: { value: (0, color_1.Color)(0x1A5653) } }, { tag: 'polymer' });
                    blobString = localStorage.getItem('blobSeq');
                    blobArray = blobString === null || blobString === void 0 ? void 0 : blobString.split(',');
                    p_arr = [];
                    tempHArray = [];
                    h_arr = [];
                    s_arr = [];
                    if (typeof blobArray != 'undefined') {
                        for (i = 0; i < blobArray.length; i++) {
                            blobIndex = i + 1;
                            nextArrayIndex = i + 1;
                            if (blobArray[i] == 'h' && blobArray[nextArrayIndex] != 'p' && blobArray[nextArrayIndex] != 's') {
                                tempHArray.push(blobIndex);
                            }
                            else if (blobArray[i] == 'h') {
                                h_arr.push(tempHArray);
                            }
                            else if (blobArray[i] == 'p') {
                                p_arr.push(blobIndex);
                            }
                            else if (blobArray[i] == 's') {
                                s_arr.push(blobIndex);
                            }
                            ;
                        }
                        ;
                    }
                    ;
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
                    ;
                    for (_b = 0, s_arr_1 = s_arr; _b < s_arr_1.length; _b++) {
                        val_s = s_arr_1[_b];
                        sel = builder_1.MolScriptBuilder.struct.generator.atomGroups({
                            'residue-test': builder_1.MolScriptBuilder.core.rel.eq([builder_1.MolScriptBuilder.struct.atomProperty.macromolecular.label_seq_id(), val_s]),
                        });
                        update.to(structure);
                        for (_c = 0, h_arr_2 = h_arr; _c < h_arr_2.length; _c++) {
                            val_h = h_arr_2[_c];
                            sel_1 = builder_1.MolScriptBuilder.struct.generator.atomGroups({
                                'residue-test': builder_1.MolScriptBuilder.core.set.has([builder_1.MolScriptBuilder.set.apply(builder_1.MolScriptBuilder, val_h), builder_1.MolScriptBuilder.ammp('label_seq_id')])
                            });
                            update.to(structure)
                                .apply(transforms_1.StateTransforms.Model.StructureSelectionFromExpression, { label: 'Surroundings', expression: sel_1 })
                                .apply(transforms_1.StateTransforms.Representation.StructureRepresentation3D, (0, structure_representation_params_1.createStructureRepresentationParams)(plugin, structure.data, {
                                type: 'gaussian-surface',
                                color: 'uniform',
                                colorParams: { value: (0, color_1.Color)(0x0096FF) },
                                typeParams: { alpha: 1.0 }
                            }));
                        }
                        ;
                        update.commit();
                    }
                    ;
                    return [2 /*return*/];
            }
        });
    });
}
function createPlugin(parent) {
    return __awaiter(this, void 0, void 0, function () {
        var defaultSpec, plugin, elementsArray;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    defaultSpec = (0, spec_1.DefaultPluginUISpec)();
                    return [4 /*yield*/, (0, mol_plugin_ui_1.createPluginUI)({
                            target: parent,
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
                    plugin = _a.sent();
                    createBlobRepresentation(plugin);
                    elementsArray = document.querySelectorAll('.mutatebox,#snp_id,#residue_type,#domain_threshold_user_box,#domain_threshold_user_slider,#cutoff_user_box,#cutoff_user_slider,.checkbox,#hydro_scales');
                    elementsArray.forEach(function (elem) {
                        elem.addEventListener('change', function () {
                            setTimeout(function () {
                                createBlobRepresentation(plugin);
                            }, 1000);
                        });
                    });
                    return [2 /*return*/];
            }
        });
    });
}
;
createPlugin(document.getElementById('app')); // app is a <div> element with position: relativeE
