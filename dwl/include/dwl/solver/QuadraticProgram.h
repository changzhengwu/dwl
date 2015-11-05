#ifndef DWL__SOLVER__QUADRATIC_PROGRAM__H
#define DWL__SOLVER__QUADRATIC_PROGRAM__H


namespace dwl
{

namespace solver
{

/**
 @class QuadraticProgram
 @brief Abstract class to define the optimization algorithm for Model Predictive Control. This class
 acts as an interface to use a defined optimization solver software as a part of this library in
 order to provide different solver options for the end user to solve the basic optimization problem
 that rises in MPC. As more solvers are adapted to this library with this class, more options to
 try different optimization methods are available to select the most suitable one depending on
 each case. The basic
 \f{eqnarray*}{
	\mbox{Minimize} \; F(x) && \\
	\mbox{subject to} \; G(x) & = & 0 \\
	H(x) & \geq & 0
\f}
 As more solvers are adapted to this library with this class, more options to try different
 optimization methods are available to select the most suitable one depending on each case.
*/
class QuadraticProgram
{
	public:
		/** @brief Constructor function */
		QuadraticProgram();

		/** @brief Destructor function */
		virtual ~QuadraticProgram();

		/**
	 	 * @brief Function to perform the initialization of optimizer, if this applies.
	 	 * @param unsigned int Number of variables of the QP problem
	 	 * @param unsigned int Number of constraints of the QP problem
	 	 * @return Label that indicates if the initialization of the optimizer is successful
		 */
		virtual bool init(unsigned int num_variables,
				  	  	  unsigned int num_constraints) = 0;
				
		/**
	 	 * @brief Function to compute the QP solution
	 	 * @param const Eigen::MatrixXd& Hessian matrix
	 	 * @param const Eigen::VectorXd Gradient vector
	 	 * @param const Eigen::MatrixXd& Constraint matrix
	 	 * @param const Eigen::VectorXd Low bound vector
	 	 * @param const Eigen::VectorXd Upper bound vector
	 	 * @param const Eigen::VectorXd Low constraint vector
	 	 * @param const Eigen::VectorXd Upper constraint vector
	 	 * @param double CPU-time for computing the optimization. If NULL, it provides on output
	 	 * the actual calculation time of the optimization problem.
	 	 * @return bool Label that indicates if the computation of the optimization is successful
		 */
		virtual bool compute(const Eigen::MatrixXd& hessian,
							 const Eigen::VectorXd& gradient,
							 const Eigen::MatrixXd& constraint_mat,
							 const Eigen::VectorXd& lower_bound,
							 const Eigen::VectorXd& upper_bound,
							 const Eigen::VectorXd& lower_constraint,
							 const Eigen::VectorXd& upper_constraint,
							 double cputime) = 0;
				
		/**
	 	 * @brief Get the vector of optimal or sub-optimal solutions calculated by the
	 	 * dwl::solver::QuadraticProgram::computeOpt() function (optimality of the function is defined
	 	 * by the solver that is adapted).
	 	 * @return double* Optimal solution
		 */
		Eigen::VectorXd& getOptimalSolution();

		/**
	 	 * @brief Get the number of variables, i.e inputs * horizon
	 	 * @return unsigned int Number of variables
		 */
		unsigned int getNumberOfVariables() const;

		/**
	 	 * @brief Get the number of constraints
	 	 * @return unsigned int Number of constraints
		 */
		unsigned int getNumberOfConstraints() const;


	protected:
		/** @brief Label that indicates if QP solver had been initialized */
		bool initialized_solver_;

		/** @brief Number of variables */
		unsigned int variables_;

		/** @brief Number of constraints */
		unsigned int constraints_;

		/** @brief Solution of the QP problem */
		Eigen::VectorXd solution_;
};

} //@namepace solver
} //@namespace dwl

#endif

