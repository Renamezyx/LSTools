<template>
    <el-table :data="users" style="width: 100%" max-height="600">
        <el-table-column fixed prop="date" label="Date" width="150" sortable />
        <el-table-column prop="name" label="Name" width="120" />
        <el-table-column prop="stats" label="Stats" width="120" sortable>
            <template #default="scope">
                <el-tag type="primary" effect="light" v-if="scope.row.stats == 0">{{ stats_format(scope.row.stats)
                    }}</el-tag>
                <el-tag type="success" effect="light" v-if="scope.row.stats == 1">{{ stats_format(scope.row.stats)
                    }}</el-tag>
                <el-tag type="danger" effect="light" v-if="scope.row.stats == -1">{{ stats_format(scope.row.stats)
                    }}</el-tag>
            </template>
        </el-table-column>
        <el-table-column prop="phone" label="phone" width="120" />
        <el-table-column prop="cookies" label="Cookies" width="600" show-overflow-tooltip />
        <el-table-column fixed="right" label="Operations" min-width="220">
            <template #default="scope">
                <el-button link type="primary" size="small" @click.prevent="push(scope.row.id)">
                    Push
                </el-button>
                <el-button link type="info" size="small" @click.prevent="openDrawer('edit', scope.row)">
                    Edit
                </el-button>
                <el-button link type="danger" size="small" @click.prevent="del(scope.row.id)">
                    Del
                </el-button>
            </template>
        </el-table-column>
    </el-table>
    <el-button class="mt-4" style="width: 100%" @click="openDrawer('add')">
        Add Item
    </el-button>
    <el-drawer v-model="drawer" title="Input" :direction="direction" :before-close="handleClose">
        <el-form label-width="100px">
            <el-form-item label="UserName">
                <el-input v-model="User.username" style="width: 240px" placeholder="Please input your username"
                    clearable />
            </el-form-item>

            <el-form-item label="Phone">
                <el-input v-model="User.phone" style="width: 240px" placeholder="Please input your phone number"
                    clearable />
            </el-form-item>

            <el-form-item label="Headers">
                <el-input v-model="User.headers" style="width: 240px" :autosize="{ minRows: 2, maxRows: 4 }"
                    type="textarea" placeholder="Please input your headers" />
            </el-form-item>
        </el-form>
        <template #footer>
            <div style="flex: auto">
                <el-button @click="cancelClick">cancel</el-button>
                <el-button type="primary" @click="confirmClick">confirm</el-button>
            </div>
        </template>
    </el-drawer>

</template>

<script lang="ts" setup>
import { ref, reactive } from 'vue'
import type { DrawerProps } from 'element-plus'
import { ElMessageBox, ElMessage } from 'element-plus'
import service from '@/utils/request'

const User = reactive({
    "id": 0,
    "username": "",
    "phone": "",
    "headers": ""
})

const drawer = ref(false)
var drawer_type = "add"
const direction = ref<DrawerProps['direction']>('rtl')

const users = ref([])

const push = (id: number) => {
    console.log("push")
    console.log(id)
}


const del = (id: number) => {
    console.log("del")
    ElMessageBox.confirm(
        '确认删除?',
        'Warning',
        {
            confirmButtonText: '确认',
            cancelButtonText: '取消',
            type: 'warning',
        }
    )
        .then(async () => {
            try {
                const response = await service.post('/users/delete', {
                    id: id
                })
                console.log('Response:', response.data.code)
                if (response.data.code == 0) {
                    select()
                }
            } catch (error) {
                console.error('Request failed:', error)
            }
        })

}

const openDrawer = (type: string, user: any | undefined = undefined) => {
    drawer_type = type
    if (type == "add") {
        User.username = ""
        User.phone = ""
        User.headers = ""
        drawer.value = true
    }
    else if (type == "edit") {
        User.id = user.id
        User.username = user.username
        User.phone = user.phone
        User.headers = user.headers
        drawer.value = true
    }
}
const stats_format = (stats: number) => {
    switch (stats) {
        case 0:
            return "空闲"
        case 1:
            return "直播中"
        case -1:
            return "cookies过期"
        default:
            return "未知"
    }
}

const handleClose = (done: () => void) => {
    ElMessageBox.confirm('Are you sure you want to close this?')
        .then(() => {
            done()
        })
        .catch(() => {
            // catch error
        })
}

const cancelClick = () => {
    drawer.value = false
    console.log("cancel")
}

const confirmClick = async () => {
    console.log("confirm")
    try {
        var response: any = {}
        if (drawer_type == "add") {
            response = await service.post('/users/insert', {
                username: User.username,
                phone: User.phone,
                headers: User.headers
            })
        } else if (drawer_type == "edit") {
            response = await service.post('/users/update', {
                id: User.id,
                username: User.username,
                phone: User.phone,
                headers: User.headers
            })
        }
        console.log('Response:', response.data.code)
        if (response.data.code == 0) {
            select()
        }
        drawer.value = false
    } catch (error) {
        console.error('Request failed:', error)
    }
}

const select = async (phone: number | undefined = undefined) => {
    console.log("select")
    try {
        const response = await service.get('/users/select', {
            params: {
                phone: phone
            }
        })
        users.value = response.data.data.map((item: any) => ({
            ...item,  // 保留原始属性
            date: new Date(item.update_time * 1000).toLocaleDateString(),
            cookies: item.headers,
            stats: 0,
            phone: item.phone,
            name: item.username,
        }))
        console.log('Response:', response.data.code)
    } catch (error) {
        console.error('Request failed:', error)
    }
}

select()
</script>

<style scoped></style>