import llvm.core	# core library
import llvm.ee		# execution engine (JIT/interpreter)

module = llvm.core.Module.new('null_module') ; print module
# JIT compiler / interpreter
engine = llvm.ee.ExecutionEngine.new(module) ; print engine
