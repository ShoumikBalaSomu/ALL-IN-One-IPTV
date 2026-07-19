package com.iptv.proxy.data

import androidx.room.Database
import androidx.room.RoomDatabase

// Stub entity for scaffolding
@androidx.room.Entity
data class ChannelEntity(
    @androidx.room.PrimaryKey(autoGenerate = true) val id: Int,
    val name: String
)

@androidx.room.Dao
interface ChannelDao {
    @androidx.room.Query("SELECT * FROM ChannelEntity")
    fun getAll(): List<ChannelEntity>
}

@Database(entities = [ChannelEntity::class], version = 1, exportSchema = false)
abstract class AppDatabase : RoomDatabase() {
    abstract fun channelDao(): ChannelDao
}
