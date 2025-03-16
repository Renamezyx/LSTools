<template>
    <el-table :data="scripts" style="width: 100%" max-height="600">
        <el-table-column fixed prop="date" label="Date" width="150" sortable />
        <el-table-column prop="script_name" label="Script Name" width="120" />
        <el-table-column prop="script_type" label="Script Type" width="120" sortable>
            <template #default="scope">
                <el-tag type="primary" effect="light" v-if="scope.row.script_type == 0">{{ script_type_format(scope.row.script_type)
                    }}</el-tag>
                <el-tag type="info" effect="light" v-if="scope.row.script_type == 1">{{ script_type_format(scope.row.script_type)
                    }}</el-tag>
            </template>
        </el-table-column>
        <el-table-column prop="script_prames" label="Script Prames" width="120" />
        <el-table-column prop="script_content" label="Script Content" width="600" show-overflow-tooltip />
        <el-table-column fixed="right" label="Operations" min-width="220">
            <template #default="scope">
                <el-button link type="primary" size="small" @click="testScript(scope.row)">
                    Test
                </el-button>
                <el-button link type="info" size="small" @click="editScript(scope.row)">
                    Edit
                </el-button>
                <el-button link type="danger" size="small" @click="deleteScript(scope.row)">
                    Del
                </el-button>
            </template>
        </el-table-column>
    </el-table>

    <el-button class="mt-4" style="width: 100%" @click="addScript">
        Add Script
    </el-button>

    <el-drawer v-model="drawer" title="Script Input" :before-close="handleClose">
        <el-form label-width="140px">
            <el-form-item label="Script Name">
                <el-input v-model="script.script_name" style="width: 240px" placeholder="Enter script name" clearable />
            </el-form-item>

            <el-form-item label="Script Params">
                <el-input v-model="script.script_prames" style="width: 240px" placeholder="Enter script params"
                    clearable />
            </el-form-item>

            <el-form-item label="Script Content">
                <el-input v-model="script.script_content" style="width: 240px" :autosize="{ minRows: 2, maxRows: 4 }"
                    type="textarea" placeholder="Enter script content" />
            </el-form-item>
        </el-form>

        <template #footer>
            <div style="flex: auto">
                <el-button @click="cancelClick">Cancel</el-button>
                <el-button type="primary" @click="confirmClick">Confirm</el-button>
            </div>
        </template>
    </el-drawer>
</template>

<script>
import { ElMessageBox, ElMessage } from 'element-plus';

export default {
    name: 'ScriptManager',
    data() {
        return {
            drawer: false,
            script: {
                date: '',
                script_type: '',
                script_name: '',
                script_content: '',
                script_prames: ''
            },
            scripts: [
                {
                    date: '2021-09-01',
                    script_name: 'Test Script',
                    script_type: 0,
                    script_content: 'console.log("Hello World")',
                    script_prames: '--verbose'
                }
            ],
            editingIndex: null,
        };
    },
    methods: {
        handleClose() {
            ElMessageBox.confirm('Are you sure you want to close this?')
                .then(() => {
                    this.drawer = false;
                })
                .catch(() => {
                    // 用户取消关闭操作
                });
        },
        cancelClick() {
            this.drawer = false;
        },
        confirmClick() {
            if (this.editingIndex !== null) {
                this.scripts[this.editingIndex] = { ...this.script };
                this.editingIndex = null;
                ElMessage.success("Script updated successfully!");
            } else {
                this.scripts.push({ ...this.script, date: new Date().toISOString().split("T")[0] });
                ElMessage.success("Script added successfully!");
            }
            this.drawer = false;
            this.resetForm();
        },
        addScript() {
            this.editingIndex = null;
            this.resetForm();
            this.drawer = true;
        },
        editScript(row) {
            this.editingIndex = this.scripts.indexOf(row);
            this.script = { ...row };
            this.drawer = true;
        },
        deleteScript(row) {
            ElMessageBox.confirm('Are you sure you want to delete this script?')
                .then(() => {
                    this.scripts = this.scripts.filter(script => script !== row);
                    ElMessage.success("Script deleted successfully!");
                })
                .catch(() => {
                    // 取消删除
                });
        },
        testScript(row) {
            ElMessage.info(`Testing script: ${row.script_name}`);
            console.log("Executing script:", row.script_content);
        },
        resetForm() {
            this.script = {
                date: '',
                script_name: '',
                script_content: '',
                script_prames: ''
            };
        },
        script_type_format: (type) => {
            switch (type) {
                case 0:
                    return "safe";
                case 1:
                    return "custom";
                default:
                    return "unknown";
            }
        }
    },
    computed: {

    }
};
</script>

<style scoped>
/* 添加一些基本样式 */
.el-table {
    margin-bottom: 20px;
}
</style>
