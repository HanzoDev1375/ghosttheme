const val Mod = 0

const val unMod = 0

class Models {

    fun item(md: Int) = return md

    fun user(model: Model): List<Model> {
        return List<Model>
    }

}

fun main() {
    println("hello")
}

data class Model(var user: Int, var f: String)
